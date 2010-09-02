from XMLModel import XMLModel
from rightscale.util import ElementTreeValueOK

class Tag(XMLModel):
  _name = None

  def __str__(self):
    return "%s" % (self._name)

  @property
  def name(self):
    return self._name

  @name.setter
  @ElementTreeValueOK
  def name(self, value):
    self._name = value

  ELEMENTS = {
    "name": name, 
  }
# class Tag

