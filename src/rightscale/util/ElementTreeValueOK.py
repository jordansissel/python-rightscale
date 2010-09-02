import xml.etree.ElementTree as ElementTree

# TODO(sissel): Refactor
XMLCLASS = ElementTree.XML("<a />").__class__

class ElementTreeValueOK(object):
  """ A decorator class that takes the 2nd arg and, if an ElementTree, use
  the text value. """

  def __init__(self, method):
    self.method = method

  def __call__(self, *args, **kwds):
    if len(args) > 1 and isinstance(args[1], XMLCLASS):
      self.method(args[0], args[1].text, *args[2:], **kwds)
    else:
      self.method(*args, **kwds)

