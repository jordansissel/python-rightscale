import xml.etree.ElementTree as ElementTree
from xml.etree.ElementTree import XML, Element, SubElement

# TODO(sissel): Refactor
import xml.etree.ElementTree as ElementTree
XMLCLASS = ElementTree.XML("<a />").__class__

class XMLModel(object):
  # ElementTree uses hidden classes for the nodes, so let's get that class.

  rsapi = None

  cache = dict()

  def __init__(self, data=None, rsapi=None):
    self.rsapi = rsapi
    self.tainted = dict()

    # Save the args so we can refresh later if asked.
    self._init_data = {
        "data": data,
        "rsapi": rsapi,
    }
    if isinstance(data, str):
      if data.startswith("https://"):
        cachekey = data
        if cachekey in self.cache:
          response, content =  self.cache[cachekey]
        else:
          response, content = self.rsapi.request(data)

        # Cache results. It'd be cool to cache objects, but
        # we can't 'return' from __init__ so we'd need to move to the
        # factory pattern to get this done :(
        self.cache[cachekey] = (response, content)
        self.from_xml_string(content)
      else:
        self.from_xml_string(data)
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
    super(Servers, self).__init__(**self._init_data)
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

# class XMLModel

