from XMLModel import XMLModel
from rightscale.util import ElementTreeValueOK

class Status(XMLModel):
    """ Provides a view of the status of any running jobs that you may have in
        your account. The most common use of this resource is to check the
        status of the execution of a RightScript.
        
        See http://support.rightscale.com/15-References/RightScale_API_Reference_Guide/02-Management/03-Statuses
        for details.
    """
    _state = None
    _description = None
    _href = None

    @property
    def state(self):
        """ State of script execution: "queued", "in progress", "aborted",
            "completed", "failed"
        """
        return self._state

    @state.setter
    @ElementTreeValueOK
    def state(self, value):
        self._state = value
    
    @property
    def description(self):
        return self._description
    
    @description.setter
    @ElementTreeValueOK
    def description(self, value):
        self._description = value
    
    @property
    def href(self):
        return self._href

    @href.setter
    @ElementTreeValueOK
    def href(self, value):
        self._href = value


    ELEMENTS = {
        'state': state,
        'description': description,
        'href': href
    }

# class Status
