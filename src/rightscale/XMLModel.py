import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import XML, Element, SubElement
from xml.parsers.expat import ExpatError

# TODO(sissel): Refactor
import xml.etree.ElementTree as ElementTree
XMLCLASS = ElementTree.XML("<a />").__class__

class InvalidResponse(Exception):
  def __init__(self, response, content, exception):
    self.response = response
    self.content = content
    self.exception = exception

    self.message = "\n".join([
      "Original exception: %s" % (self.exception),
      "Response: %s" % response,
      "Content: %s" % content,
    ])
  # def __init__

  def __str__(self):
    return self.message
  # def __str__
class XMLModel(object):
  # ElementTree uses hidden classes for the nodes, so let's get that class.

  rsapi = None

  cache = dict()

  def __init__(self, data=None, rsapi=None, use_cache=True):
    self.rsapi = rsapi
    self.tainted = dict()

    # Save the args so we can refresh later if asked.
    self._init_data = {
        "data": data,
        "rsapi": rsapi,
        "use_cache": False,
    }
    if isinstance(data, str):
      if data.startswith("https://"):
        cachekey = data
        if use_cache and cachekey in self.cache:
          response, content =  self.cache[cachekey]
        else:
          response, content = self.rsapi.request(data)

        # Cache results. It'd be cool to cache objects, but
        # we can't 'return' from __init__ so we'd need to move to the
        # factory pattern to get this done :(
        if use_cache:
          self.cache[cachekey] = (response, content)
        try:
          self.from_xml_string(content)
        except ExpatError, e:
          raise InvalidResponse(response, content, e)
      else: # else, data is probably xml.
        try:
          self.from_xml_string(data)
        except ExpatError, e:
          raise InvalidResponse(None, data, e)
    # ElementTree uses hidden classes, so we can't use isinstance, try
    # duck typing-ish instead...
    elif isinstance(data, XMLCLASS):
      self.from_xml_tree(data)
  # def __init__

  def __iter__(self):
    for name in self.ELEMENTS:
      obj = self.ELEMENTS[name]
      if isinstance(obj, property):
        yield (name, obj.fget(self))
      else:
        yield (name, obj(self))

  """ Refresh this object. If the data used to create this object was a URL
      then it will be fetched again and this object will be updated with the
      result.  """
  def refresh(self):
    self.__init__(**self._init_data)
  # def refresh

  def from_xml_string(self, string):
    tree = ElementTree.XML(string)
    self.from_xml_tree(tree)
  # def from_xml_tree

  def from_xml_tree(self, tree):
    assert len(self.ELEMENTS) > 0, "No elements known for parsing..."
    for element in tree:
      if element.tag not in self.ELEMENTS:
        #print     "Unexpected element tag '%s' in class %s" \
             #% (element.tag, type(self).__name__)
        continue

      # Call the handler for this element
      obj = self.ELEMENTS[element.tag]
      if obj is None:
        pass # ignore
      elif isinstance(obj, property):
        obj.fset(self, element)
      else:
        obj(self, element)
    # for element ...
  # def from_xml_tree

  def taint(self, what):
    self.tainted[what] = True
  # def taint

  def untaint(self, what):
    del self.tainted[what]
  # def untaint

# class XMLModel

