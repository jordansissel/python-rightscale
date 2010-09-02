from XMLModel import XMLModel
from Tag import Tag
from rightscale.util import ElementTreeValueOK

class Tags(XMLModel):
  def __init__(self, data=None, rsapi=None):
    self.tags = list()
    super(Tags, self).__init__(data, rsapi)
  # def __init__

  def __str__(self):
    return ", ".join([str(t) for t in self.tags])

  def __contains__(self, value):
    return len([t for t in self.tags if t.name == value]) > 0

  def for_resource(self, href):
    params = {
      "resource_href": href
    }
    try:
      response, content = self.rsapi.request("tags/search", parameters=params);
      self.from_xml_string(content)
    except:
      print "Failed parsing %r" % (params)
      for frame in inspect.stack():
        print frame
      #print response
      #print content
  # def for_resource

  def add_tag(self, data):
    tag = Tag(data, self.rsapi)
    self.tags.append(tag)
  # def add_tag

  # override XMLModel's __iter__ and give all tags.
  def __iter__(self):
    for t in self.tags:
      yield t
  # def __iter__

  ELEMENTS = {
    "tag": add_tag
  }
# class Tags

