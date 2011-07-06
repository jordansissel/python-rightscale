from XMLModel import XMLModel
from rightscale.util import ElementTreeValueOK
from rightscale.Tags import Tags

# TODO(sissel): Refactor
import xml.etree.ElementTree as ElementTree
XMLCLASS = ElementTree.XML("<a />").__class__

class ServerTemplate(XMLModel):
  _tags = None
  _href = None

  @property
  def tags(self):
    if self._tags is None:
      self._tags = Tags(rsapi=self.rsapi)
      #print "Looking up %s" % self.href
      self._tags.for_resource(self.href)
    return self._tags

  @tags.setter
  @ElementTreeValueOK
  def tags(self, value):
    self._tags = Tags(value, self.rsapi)

  @property
  def href(self):
    return self._href

  @href.setter
  @ElementTreeValueOK
  def href(self, value):
    self._href = value

  @property
  def nickname(self):
    return self._nickname

  @nickname.setter
  @ElementTreeValueOK
  def nickname(self, value):
    self._nickname = value

  ELEMENTS = {
    "href": href,
    "nickname": nickname,
  }
# class ServerSettings

