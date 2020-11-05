class Request:
    """
    Encapsulates request handling
    _zip_, _state_, _county_ are used internally to capture the values used to initialize a Request instance
    zip, state, county are used externally and can be reset as needed for the instance 
    """
    # constants
    STATE_COUNTY=1
    STATE_ONLY=2
    ZIPCODE=3

    def __init__(self,request):
        self._zip_ = request.POST.get("zipCode")
        self.zip = self._zip_
        self._state_ = request.POST.get("state")
        self.state = self._state_
        self._county_ = request.POST.get("county")
        self.county = self._county_

    def search_type(self):
        if len(self._state_) > 0 and len(self._county_) > 0:
            # this is a state/county search
            return Request.STATE_COUNTY
        if len(self._state_) > 0 and len(self._county_) == 0:
            # this is a state/county search
            return Request.STATE_ONLY
        if len(self._zip_) > 0:
            # this is a state/county search
            return Request.ZIPCODE