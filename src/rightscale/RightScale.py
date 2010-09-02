import base64
import sys
from urllib import urlencode
from rightscale.util import ElementTreeValueOK
from rightscale import Servers
from rightscale import Deployments
from rightscale import Server

# TODO(sissel): better error handling and reporting.
# TODO(sissel): document
# TODO(sissel): tests

# Requires >= python 2.5
import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import XML, Element, SubElement

# third party
import httplib2
import netifaces

#httplib2.debuglevel=1

# TODO(sissel): RightScale cookies expire at an unknown interval so we won't use
# cookies until we know they work. Bug filed with RightScale.
DISABLE_COOKIES = True

class RightScale(object):
  """ General interface to RightScale. 

      We will support cookies in the future once RightScale's treatment of
      cookies is more well documented and reliable.
  """

  def __init__(self, account=None, user=None, password=None, cookie=None):
    """ Configures a new RightScale object. 

        Required arguments:
          account user, password

        Cookies are not currently supported.
    """
    self._http = httplib2.Http()
    self._is_authenticated = False
    self._headers = {
      "X-API-VERSION": "1.0"
    }

    assert account is not None, "No account provided"
    if DISABLE_COOKIES:
      assert cookie is None, "Cookies are not supported. We are waiting on RightScale to clarify and fix the login api before cookies will work again."

    self.account = account

    # Validate
    if cookie is None:
      assert not (user is None or password is None), "Requires user and password OR cookie"
      self.user = user
      self.password = password
      if DISABLE_COOKIES:
        self._is_authenticated = True
        auth_string = base64.encodestring("%s:%s" % (self.user, self.password))
        self._headers["Authorization"] = "Basic %s" % auth_string
    else:
      assert user is None and password is None, "Requires user and password OR cookie"
      self._headers["Cookie"] = cookie
      self._is_authenticated = True
      self.user = None
      self.password = None
  # def __init__

  def request(self, path, parameters=None, method="GET", body=None):
    """ Make a request through the rightscale api. 
        This is generally only used internally but is made available
        public in case you need it. 
        
        Arguments:
        path - partial or full url for the rightscale api. If the url is partial,
          it is assumed to be relative to https://my.rightscale.com/api/acct/<account>/
        parameters - dict. parameters to pass on the url. 
        method - http method. Defaults to GET
        body - request body, also urlencoded like 'parameters' is. If specified, this
          will cause the Content-Type to get set to application/x-www-form-urlencoded.
        """
    if path.startswith("https://"):
      url = path
    else:
      url = "https://my.rightscale.com/api/acct/%d/%s" % (self.account, path)
        
    if parameters:
      url = "%s?%s" % (url, urlencode(parameters, doseq=1))
    if body:
      body = urlencode(body)
      self._headers["Content-Type"] = "application/x-www-form-urlencoded"
      self._headers["Content-Length"] = "%s" % len(body)
    else:
      self._headers["Content-Length"] = "0"
      if "Content-Type" in self._headers:
        del self._headers["Content-Type"]
    #print "Request: %s %s" % (method, url)
    #print self._headers
    response, content = self._http.request(url, headers=self._headers,
        method=method, body=body)
    return response, content

  def ensure_authenticated(self):
    """ Ensure we are authenticated. """
    if not self._is_authenticated:
      self.authenticate()
  # def ensure_authenticated

  def authenticate(self):
    """ Authenticate with RightScale's API """
    if DISABLE_COOKIES:
      return
    if self.user is None or self.password is None:
      raise Exception("No user and password known. Cannot authenticate.")
    auth_string = base64.encodestring("%s:%s" % (self.user, self.password))
    self._headers["Authorization"] = "Basic %s" % auth_string
    response, content = self.request("login")
    del self._headers["Authorization"]
    self._headers["Cookie"] = response['set-cookie']
    self._is_authenticated = True
  # def authenticate

  @property
  def deployments(self):
    """ Query deployments in RightScale.
        http://support.rightscale.com/15-References/RightScale_API_Reference_Guide/02-Management/01-Deployments

        Returns a Deployments object.  """
    self.ensure_authenticated()
    response, content = self.request("deployments.xml")
    deployments = Deployments(content, self)
    return deployments
  # def deployments

  @property
  def servers(self):
    """ Query servers in RightScale.
        http://support.rightscale.com/15-References/RightScale_API_Reference_Guide/02-Management/02-Servers

        Returns a Servers object """
    self.ensure_authenticated()
    response, content = self.request("servers.xml")
    return Servers(content, self)
  # def servers

  def whoami(self):
    """ Try to find myself (this server) in RightScale.
        It will query for any server matching any IP on this host.

        Returns a Server object if found, None otherwise. """
    # This isn't likely the most optimal way to find the server, but
    # it's not bad either.  We could query by aws_id which would only require 1
    # query, not 2n where n is the number of addresses on the system.
    self.ensure_authenticated()
    for interface in netifaces.interfaces():
      addresses = netifaces.ifaddresses(interface)
      if netifaces.AF_INET not in addresses:
        continue
      for address in addresses[netifaces.AF_INET]:
        for type in ("ip_address", "private_ip_address"):
          params = { "filter": "%s=%s" % (type, address["addr"]) }
          response, content = self.request("servers.xml", parameters=params)
          servers = Servers(content, self)
          if len(servers) > 0:
            return servers[0]
        # for type ...
      # for address ...
    # for interface ...

    # If we get here, no server was found.
    return None
  # def whoami

  def save_tags(self, resource, tags):
    """ Save tags for a given resource. This is normally an internal method.

        This method will remove all tags not specified in the tags argument.

        If you want to save tags for a Server, for example, modify the tags
        for that server then invoke Server.save()

        Arguments:
        resource - the resource object to modify (Server, etc)
        tags - array of tags to save """
    oldtags = Tags(rsapi=self)
    for url in [resource.href, resource.current_instance_href]:
      oldtags.for_resource(url)
      #print [x.name for x in oldtags.tags]
      to_remove = [x.name for x in oldtags.tags if x.name not in tags]

      # Delete tags not set
      params = {
        "resource_href": url,
        "tags[]": to_remove
      }
      response, content = self.request("tags/unset", params, method="PUT")

      # Add our new tags
      params["tags[]"] = tags
      response, content = self.request("tags/set", params, method="PUT")
    # for url in ...
  # def save_tags

  def search(self, filterstring):
    """ Search for servers by a filter string. 
        See http://support.rightscale.com/15-References/RightScale_API_Reference_Guide/02-Management/02-Servers
    
        This method will improve in usability in the future.
        """
    # TODO(sissel): add keyword arguments for things to search by.
    self.ensure_authenticated()
    params = { "filter": filterstring }
    response, content = self.request("servers.xml", parameters=params)
    print response
    print content
    servers = Servers(content, self)
    return servers
  # def search

  def search_by_tags(self, tags_list, match_all=False):
    """ Search for servers by tags
    
        Arguments:
          tags_list - list of strings that are tags to search for
          match_all - if true, require all tags to match
        Returns:
          Servers object
        """
    self.ensure_authenticated()
    params = {
      "resource_type": "server",
      "tags[]": tags_list,
      "match_all": ["false", "true"][match_all]
    }
    response, content = self.request("tags/search", parameters=params);
    servers = Servers(content, self)
    return servers
  # def search

  @property
  def cookie(self):
    if "Cookie" in self._headers:
      return self._headers["Cookie"]
    else:
      return None
  # def cookie
# class RightScale
