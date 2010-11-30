from XMLModel import XMLModel
from Server import Server
from rightscale.util import ElementTreeValueOK

class Servers(XMLModel):
  def __init__(self, data=None, rsapi=None):
    #self.servers = dict()
    self.servers = list()
    super(Servers, self).__init__(data, rsapi)
  # def __init__

  def __len__(self):
    return len(self.servers)
  # def __len__

  def __getitem__(self, index):
    return self.servers[index]
  # def __getitem__

  def __iter__(self):
    #return iter(self.servers.values())
    return iter(self.servers)
  # def __iter__

  def add_server(self, data):
    server = Server(data, self.rsapi)
    #print "Got server: %s" % (server.nickname)
    self.servers.append(server)
    #self.servers[server.nickname] = server
  # def add_server

  ELEMENTS = {
    "server": add_server,
  }
# class Servers
