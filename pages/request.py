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
        Initialize the Request class instance and parse key info from the request
        to set member data. 
        """
        self.request = request

        if request.POST.get("zipCode")!=None:
            self.__zip = request.POST.get("zipCode")
        else:
            self.__zip = ''
        self.zip = self.__zip
        
        if request.POST.get("state")!=None:           
            self.__state = request.POST.get("state")
        else:
            self.__state = ''
        self.state = self.__state
        
        if request.POST.get("countyChoice")!=None:
            self.__county = request.POST.get("countyChoice")
        else:
            self.__county = ''
        self.county = self.__county

        if requestType==None:
            self.__reqType = Request.PAGE_REQUEST
        else:
            self.__reqType = Request.AJAX_REQUEST
        self.requestType = self.__reqType

        self.errMsg = ''

    def setErrMsg(self, errText):
        self.errMsg=errText

    def errConditionDetected(self):
        if len(self.errMsg) > 0:
            return True
        else:
            return False

    def search_type(self):
        if len(self.__zip) > 0:
            #this is a zip-only search
            return Request.ZIPCODE        
        if len(self.__state) > 0 and len(self.__county) > 0:
            #this is a combination state/county search
            return Request.STATE_COUNTY
        if len(self.__state) > 0 :
            #this is a state-only search
            return Request.STATE_ONLY
        if len(self.__county) > 0 :
            #this is a county-only search
            return Request.COUNTY_ONLY
