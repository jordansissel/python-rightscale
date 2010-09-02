from XMLModel import XMLModel
from rightscale.util import ElementTreeValueOK

# TODO(sissel): Refactor
import xml.etree.ElementTree as ElementTree
XMLCLASS = ElementTree.XML("<a />").__class__

class Deployment(XMLModel):
  _nickname = None
  _description = None
  _created_at = None
  _updated_at = None
  _servers = list()
  _href = None

  def __str__(self):
    return "%s" % (self.nickname)

  @property
  def nickname(self):
    return self._nickname

  @nickname.setter
  @ElementTreeValueOK
  def nickname(self, value):
    self._nickname = value

  @property
  def description(self):
    return self._description

  @description.setter
  @ElementTreeValueOK
  def description(self, value):
    self._description = value

  @property
  def created_at(self):
    return self._created_at

  @created_at.setter
  @ElementTreeValueOK
  def created_at(self, value):
    self._created_at = value

  @property
  def updated_at(self):
    return self._updated_at

  @updated_at.setter
  @ElementTreeValueOK
  def updated_at(self, value):
    self._updated_at = value

  @property
  def servers(self):
    return self._servers

  @servers.setter
  def servers(self, value):
    from Server import Server
    if isinstance(value, XMLCLASS) and value.tag == "servers":
      self._servers = list()
      for element in value:
        self.servers.append(Server(element, self.rsapi))
      # for element ...
    else:
      self._servers = value

  @property
  def href(self):
    return self._href

  @href.setter
  @ElementTreeValueOK
  def href(self, value):
    self._href = value

  @property
  def tags(self):
    from Tags import Tags
    if not self._tags:
      self._tags = Tags(rsapi=self.rsapi)
      self._tags.for_resource(self.href)
    return self._tags

  @tags.setter
  def tags(self, value):
    self.taint("tags")
    if isinstance(value, XMLCLASS) and value.tag == "tags":
      self._tags = list()
      for element in value:
        self.tags.append(Tag(element, self.rsapi))
      # for element ...
    else:
      self._tags = value
  # def tags

  ELEMENTS = {
    "nickname": nickname,
    "updated-at": updated_at,
    "created-at": created_at,
    "description": description,
    "servers": servers,
    "href": href,
    "tags": tags,
  }
# class Deployment
