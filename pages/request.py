class Request:
    """
    Encapsulates request handling
    _zip_, _state_, _county_ are used internally to capture the values used to initialize a Request instance
    zip, state, county are used externally and can be reset as needed for the instance 
    """
    # constants
    STATE_COUNTY=1
    STATE_ONLY=2
    COUNTY_ONLY=3
    ZIPCODE=4
    AJAX_REQUEST=5
    PAGE_REQUEST=6

 
    def __init__(self,request, requestType=None):
        """
        Initialize the Request class instance
        """
        self._request_ = request

        if request.POST.get("zipCode")!=None:
            self._zip_ = request.POST.get("zipCode")
        else:
            self._zip_ = ''
        self.zip = self._zip_
        
        if request.POST.get("state")!=None:           
            self._state_ = request.POST.get("state")
        else:
            self._state_ = ''
        self.state = self._state_
        
        if request.POST.get("countyChoice")!=None:
            self._county_ = request.POST.get("countyChoice")
        else:
            self._county_ = ''
        self.county = self._county_

        if requestType==None:
            self._reqType_ = Request.PAGE_REQUEST
        else:
            self._reqType_ = Request.AJAX_REQUEST
        self.requestType = self._reqType_

    def search_type(self):
        if len(self._zip_) > 0:
            #this is a zip-only search
            return Request.ZIPCODE        
        if len(self._state_) > 0 and len(self._county_) > 0:
            #this is a combination state/county search
            return Request.STATE_COUNTY
        if len(self._state_) > 0 :
            #this is a state-only search
            return Request.STATE_ONLY
        if len(self._county_) > 0 :
            #this is a county-only search
            return Request.COUNTY_ONLY
