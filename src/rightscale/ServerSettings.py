from XMLModel import XMLModel
from rightscale.util import ElementTreeValueOK

# TODO(sissel): Refactor
import xml.etree.ElementTree as ElementTree
XMLCLASS = ElementTree.XML("<a />").__class__

class ServerSettings(XMLModel):
  _ip_address = None
  _private_ip_address = None
  _dns_name = None
  _private_dns_name = None

  def __init__(self, data=None, rsapi=None):
    if isinstance(data, XMLCLASS):
      ElementTree.dump(data)
    super(ServerSettings, self).__init__(data, rsapi)
  # def __init__

  @property
  def ip_address(self):
    return self._ip_address

  @ip_address.setter
  @ElementTreeValueOK
  def ip_address(self, value):
    self._ip_address = value

  @property
  def private_ip_address(self):
    return self._private_ip_address

  @private_ip_address.setter
  @ElementTreeValueOK
  def private_ip_address(self, value):
    self._private_ip_address = value

  @property
  def dns_name(self):
    return self._dns_name

  @dns_name.setter
  @ElementTreeValueOK
  def dns_name(self, value):
    self._dns_name = value

  @property
  def private_dns_name(self):
    return self._private_dns_name

  @private_dns_name.setter
  @ElementTreeValueOK
  def private_dns_name(self, value):
    self._private_dns_name = value

  @property
  def aws_id(self):
    try:
      return self._aws_id
    except:
      return None

  @aws_id.setter
  @ElementTreeValueOK
  def aws_id(self, value):
    self._aws_id = value

  ELEMENTS = {
    "dns-name": dns_name,
    "private-dns-name": private_dns_name,
    "private-ip-address": private_ip_address,
    "ip-address": ip_address,
    "aws-id": aws_id,
  }
# class ServerSettings

