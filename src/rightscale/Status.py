from XMLModel import XMLModel
from rightscale.util import ElementTreeValueOK

class Status(XMLModel):
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
