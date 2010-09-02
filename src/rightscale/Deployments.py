from XMLModel import XMLModel
from rightscale import Deployment
from rightscale.util import ElementTreeValueOK

class Deployments(XMLModel):
  def __init__(self, data=None, rsapi=None):
    self.deployments = dict()
    super(Deployments, self).__init__(data, rsapi)
  # def __init__

  def __len__(self):
    return len(self.deployments)
  # def __len__

  def __getitem__(self, index):
    return self.deployments[index]
  # def __getitem__

  def __iter__(self):
    return iter(self.deployments.values())
  # def __iter__

  def add_deployment(self, data):
    deployment = Deployment(data, self.rsapi)
    self.deployments[deployment.nickname] = deployment
  # def add_deployment

  ELEMENTS = {
    "deployment": add_deployment
  }
# class Deployments
