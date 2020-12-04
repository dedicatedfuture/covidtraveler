"""! @brief COVID Traveler Request package code"""

##
# @file request.py
#
# @brief request.py defines a single class Request is a bridge between the http request and the application framework.
#
# @section description_request Description
# This package defines the the Request class. This class accepts an http request when instantiated to capture the type of method
# passed (AJAX or POST) and determines what kind of search can be performed (v1.1 under development). It provides public methods
# that indicate the kind of search that was requested, if the search succeeded, and error text that can be displayed.
# - Request - the only class in the package, used for conveying request and response information between the django framework
# and the application code.
#
## @section libraries_request Libraries/Modules
# - Django imports:
# 	- None
# - Application imports:
# 	- None
#
# @section author_request Author(s)
# - Created by Team #3 on 11/29/2020.
# - Modified by Team #3 on 11/29/2020.
#
# Copyright (c) 2020 COVID Traveler Warning Team.  All rights reserved.

class Request:
    """! 
    Request accepts the http request object and parses it to determine user search intent as well as data used for th search. It also returns request response information to the caller 
    """
    # constants
    STATE_COUNTY=1
    STATE_ONLY=2
    COUNTY_ONLY=3
    ZIPCODE=4
    AJAX_REQUEST=5
    PAGE_REQUEST=6

 
    def __init__(self,request, requestType=None):
        """!
		@param request This contains a Request class object that contains the original http request and information derived from the http request. See the request package for additional
		details.

		@param requestType If populated, this parameter accepts a value that resolves to either AJAX_REQUEST or PAGE_REQUEST. This is saved for later reference if needed by application code.
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
        """!
        Sets the instance member self.errMsg from parameter errText.

		@param errText This contains the error text set by the application code if an error is encountered that should be reported to the user. 
		"""
        self.errMsg=errText

    def errorConditionDetected(self):
        """!
        Tests self.errMsg for presence of an error message - if found, the method returns True, otherwise it returns False.

		@param request This contains a Request class object that contains the original http request and information derived from the http request. 
        See the request package for additional details.

		@return Returns True iIf self.errMsg contains text indicating that an error has been reported. Otherwise, returns False.
		"""
        if len(self.errMsg) > 0:
            return True
        else:
            return False

    def search_type(self):
        """!
        Evaluates the contents of members self.__zip, self.__state and self.__county to determine the caller's request intention. 

		@return Returns a constant that indicates the type of search using the following rules in order of precedence:
        1. if zip code is populated, return Request.ZIPCODE (v1.0)   
        2. if state and county are populated, return Request.STATE_COUNTY (v1.1)
        3. if state alone is populated, return Request.STATE_ONLY (v1.1)
        4. if county alone is populated, return Request.COUNTY_ONLY (v1.1)
		"""
        if len(self.__zip) > 0:
            #This is a zip-only search
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
    
    def setContext(self, context):
        """! 
        Sets the content of the context member of the instance.
		@param context This sets the instance's render context member.
		"""
        self.context = context

    def getContext(self):
        """!
        Gets the contents of the context member of the instance. 
		@return Returns the contents of the context member of the instance.
		"""        
        return self.context
