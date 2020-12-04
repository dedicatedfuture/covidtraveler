"""! @brief COVID Traveler builder package code"""

##
# @file builder.py
#
# @brief builder.py contains code that implements the Builder design pattern to construct a response to a request using classses from pages.models, pages.request, 
# pages.persistence and pages.graphics. The Director class coordinates the construction of the response by using the SearchResultsBuilder class to populate the contents
# of the SearchResults class instance Request is a bridge between the http request and the application framework.
#
## @section description_builder Description
# This package defines the the Request class. This class accepts an http request when instantiated to capture the type of method
# passed (AJAX or POST) and determines what kind of search can be performed other than zip code (v1.1 under development). It provides public methods
# that indicate the kind of search that was requested, if the search succeeded, and error text that can be displayed.
# - Request - the only class in the package, used for conveying request and response information between the django framework
# and the application code.
#
## @section libraries_builder Libraries/Modules
# - Django/Python imports:
# 	- sys from python
# - Application imports:
# 	- Request from pages.request
#   - CovidMessages, CovidModelFactory, CovidModel, CovidLocationInfo from pages.models
#   - DjangoDB from pages.persistence
#   - GraphicsFactory, Graphic from pages.graphics
#
## @section author_builder Author(s)
# - Created by Team #3 on 11/29/2020.
# - Modified by Team #3 on 11/29/2020.
#
# Copyright (c) 2020 COVID Traveler Warning Team.  All rights reserved.

import sys
from pages.request import Request
from pages.models import CovidMessages, CovidModelFactory, CovidModel, CovidLocationInfo
from pages.persistence import DjangoDB
from pages.graphics import GraphicsFactory, Graphic
from abc import ABC, abstractmethod



# Using the Builder design pattern, the Director class manages construction of the SearchResults
class Director:
    """! 
    Director is responsible for managing the order of actions to construct the response to a Request object passed by the caller. It coordinates the effort of the builder class that is set
    by the setBuilder() method, then uses getSearchResults() to perform the detail construction of the object to be returned to the caller. 
    """
    __builder = None

    def setBuilder(self, builder):
        """! 
        This method sets the Builder class object responsible for building the object requested by the user. 
        """
        self.__builder = builder

    def getSearchResults(self, *args, **kwargs):
        """! 
        This method invokes the methods of the Builder class set by setBuilder to construct the object of interest. It returns
        """
        if 'REQUEST' in kwargs:
            self.__request = kwargs['REQUEST']
        else:
            self.__request = None        
        try:    
            searchResults = SearchResults()

            # test for data available - if not, exit early and provide error text
            if self.__builder.isDataAvailableForRequest(REQUEST=self.__request) == False:
                self.__request.setErrMsg("No data is available for zip code " + self.__request.zip)
                #SearchResults.context['msg_text']=str(covidInfoMsgs).strip('"')
                return

            # get aggregate graph
            aggGraph = self.__builder.getCovidAggregateCasesDeceased(REQUEST=self.__request)        
            searchResults.setAggregateCovid(aggGraph)
            SearchResults.context['graph1']=aggGraph

            #get monthly graph
            monthlyGraph = self.__builder.getCovidMonthlyCasesDeceased(REQUEST=self.__request)
            searchResults.setMonthlyCovid(monthlyGraph)
            SearchResults.context['graph2']=monthlyGraph
            
            #get daily cases/deceased graphs - this will be re-factored if time permits to break out cases/deceased
            dailyCasesGraph = self.__builder.getCovidDailyCases(REQUEST=self.__request)
            searchResults.setDailyCases(dailyCasesGraph)
            SearchResults.context['graph3']=dailyCasesGraph['CASES_GRAPH']
            SearchResults.context['graph4']=dailyCasesGraph['DECEASED_GRAPH']

            # #get daily deceased graph 
            # dailyDeceasedGraph = self.__builder.getCovidDailyDeceased(REQUEST=self.__request)
            # searchResults.setDailyDeceased(dailyDeceasedGraph)
            # SearchResults.context['graph4']=dailyDeceasedGraph

            #get info messages
            covidInfoMsgs = self.__builder.getCovidInfoMsgs(REQUEST=self.__request)
            searchResults.setCovidInfoMsgs(covidInfoMsgs)
            # create the msg_text dictionary element only if there is text present
            if len(covidInfoMsgs)>0:
                SearchResults.context['msg_text']=str(covidInfoMsgs).strip('"')

            #return the request object with it's context member populated if no errors
            self.__request.setContext(searchResults.getSearchContext())
            if self.__request.errorConditionDetected():
                return False
            else:
                return True
        except:
            print ("Director.getSearchResults().1 - unexpected error: ",sys.exc_info()[0])
            self.__request.setErrMsg("An unexpected error occurred performing the search for zip code ", self.__request.zip, ". Please use the contact form to report the issue.")
            return False  

class Builder(ABC):
    """! 
    Builder is an abstract class that defines methods that must be implemented by classes that inherit from Builder. 
    """
    def isDataAvailableForRequest(self, **kwargs) : pass
    """! 
    This is an abstract method for testing for available data to build an object.
    @param **kwargs This is a dictionary of name/value pairs of parameters passed to the method. Using a dictionary enables polymorphic behavior for the method.

    @return If data is found returns True, otherwise returns False
    """

    def getCovidAggregateCasesDeceased(self, **kwargs): pass
    """! 
    This is an abstract method for returning a graphical representation of Aggregate COVID Cases and Deceased data.
    @param **kwargs This is a dictionary of name/value pairs of parameters passed to the method. 

    @return If data is found returns a graph, otherwise returns None
    """

    def getCovidMonthlyCasesDeceased(self, **kwargs): pass
    """! 
    This is an abstract method for returning a graphical representation of Monthly COVID Cases and Deceased data.
    @param **kwargs This is a dictionary of name/value pairs of parameters needed by the child class. Using a dictionary enables polymorphic behavior for the method.

    @return If data is found returns a graph, otherwise returns None
    """

    def getCovidDailyCases(self, **kwargs): pass
    """! 
    This is an abstract method for returning a graphical representation of Daily COVID Cases and Deceased data (v1.0). For v1.1 it will only return Cases, not Deceased data.
    @param **kwargs This is a dictionary of name/value pairs of parameters needed by the child class. Using a dictionary enables polymorphic behavior for the method.

    @return If data is found returns a graph, otherwise returns None
    """

    def getCovidDailyDeceased(self, **kwargs): pass
    """! 
    (v1.1) This is an abstract method for returning a graphical representation of Daily COVID Deceased data.
    @param **kwargs This is a dictionary of name/value pairs of parameters needed by the child class. Using a dictionary enables polymorphic behavior for the method.

    @return If data is found returns a graph, otherwise returns None
    """

    def getCovidInfoMsgs(self, **kwargs): pass
    """! 
    This is an abstract method for testing for retrieving informational messages related to a search request.
    @param **kwargs This is a dictionary of name/value pairs of parameters passed to the method. Using a dictionary enables polymorphic behavior for the method.

    @return If data is found returns a string containing informational messages, otherwise returns a zero-length string
    """

class SearchResults:
    """! 
    SearchResults is a class that aggregates data and images used to satisfy a search request. 
    """
    context = {}

    def __init__(self):
        """! 
        The constructor for SearchResults. It sets the data members to None or an empty dictionary.
        """
        SearchResults.context = {}        
        self.__context = SearchResults.context
        self.__aggregateCovid = None
        self.__monthlyCovid = None
        self.__dailyCases = None
        self.__dailyDeceased = None
        self.__covidInfoMsgs = None
    
    def setAggregateCovid(self, aggGraph):
        """! 
        Method for setting self.__aggregateCovid to the image object passed in aggGraph.
        @param aggGraph An image object passed to the setter.
        """
        self.__aggregateCovid = aggGraph

    def setMonthlyCovid(self, monthlyGraph):
        """! 
        Method for setting self.__monthlyCovid to the image object passed in monthlyGraph.
        @param monthlyGraph An image object passed to the setter.
        """        
        self.__monthlyCovid = monthlyGraph

    def setDailyCases(self, dailyCasesGraph):
        """! 
        Method for setting self.__dailyCases to the image objects passed in dailyCasesGraph. For v1.0 both the cases and deceased daily graphs will be passed by this param.
        @param dailyCasesGraph An image object passed to the setter.
        """           
        self.__dailyCases = dailyCasesGraph
    
    def setDailyDeceased(self, dailyDeceasedGraph):
        """! 
        Method for setting self.__dailyDeceased to the image objects passed in dailyDeceasedGraph. This is dormant for v1.0, but will be activated in v1.1.
        @param dailyDeceasedGraph An image object passed to the setter.
        """   
        self.__dailyDeceased = dailyDeceasedGraph

    def setCovidInfoMsgs(self, covidInfoMsgs):
        """! 
        Method for setting self.__covidInfoMsgs to the informational message passed in covidInfoMsgs.
        @param covidInfoMsgs An list of text strings representing informational messages related to the search request. 
        """           
        self.__covidInfoMsgs = covidInfoMsgs

    def getSearchContext(self):
        """! 
        Method for returning the constructed search results rendering context to the caller.
        @return The fully constructed search results rendering context dictionary used by the Django framework to build dynamic content on a web page. 
        """          
        return SearchResults.context


class SearchResultsBuilder(Builder):
    """! 
    SearchResultsBuilder is a concrete class that provides provides methods for creating classes that construct objects needed by SearchResults, 
    then uses SearchResults' setter methods to save the results. 
    """
    def __init__(self, *args, **kwargs):
        """! 
        Constuctor for the class. It accepts and saves the Request object passed via kwargs for later use. 
        @param kwargs A dictionary of parameters passed from the caller  to the instance. This method parses the parameter named REQUEST containing the Request from the dictionary. 
        """  
        if 'REQUEST' in kwargs:
            self.__request = kwargs['REQUEST']
        else:
            self.__request = None

    def isDataAvailableForRequest(self, **kwargs):
        """! 
        Tests for whether data is avaiable for the requested search by creating an instance of CovidLocation(**kwargs) to test for data. 
        @param kwargs A dictionary of parameters passed from the caller to the instance. This method passes kwargs to the constructor of CovidLocation().
        """         
        dataAvailable = CovidLocation(**kwargs)
        return dataAvailable.isDataAvailable()
    
    def getCovidInfoMsgs(self, **kwargs): 
        """! 
        Checks for and retrieves informational messages for the Request by creating an instance of CovidInfoMsgs(**kwargs). 
        @param kwargs A dictionary of parameters passed from the caller  to the instance. This method passes kwargs to the constructor of CovidInfoMsgs().
        """          
        getCovidInfoMsgs = CovidInfoMsgs(**kwargs)
        return getCovidInfoMsgs.getMsgText()

    def getCovidAggregateCasesDeceased(self, **kwargs): 
        """! 
        Retrieves the graphic image for the Request by creating an instance of CovidAggregateCasesDeceased(**kwargs) and generating the image. 
        @param kwargs A dictionary of parameters passed from the caller  to the instance. This method passes kwargs to the constructor of CovidAggregateCasesDeceased().
        """           
        covidAggregate = CovidAggregateCasesDeceased(**kwargs)
        return covidAggregate.getImage()        

    def getCovidMonthlyCasesDeceased(self, **kwargs): 
        """! 
        Retrieves the graphic image for the Request by creating an instance of CovidMonthlyCasesDeceased(**kwargs) and generating the image. 
        @param kwargs A dictionary of parameters passed from the caller  to the instance. This method passes kwargs to the constructor of CovidMonthlyCasesDeceased().
        """        
        covidMonthly = CovidMonthlyCasesDeceased(**kwargs)
        return covidMonthly.getImage()

    def getCovidDailyDeceased(self, **kwargs): 
        """! 
        (v1.1) Retrieves the graphic image for the Request by creating an instance of CovidDailyDeceased(**kwargs) and generating the image. This method is dormant 
        in v1.0. 
        @param kwargs A dictionary of parameters passed from the caller  to the instance. This method passes kwargs to the constructor of CovidDailyDeceased().
        """        
        covidDailyDeceased = CovidDailyDeceased(**kwargs)
        return covidDailyDeceased.getImage()

    def getCovidDailyCases(self, **kwargs): 
        """! 
        Retrieves the graphic image for the Request by creating an instance of CovidDailyCases(**kwargs) and generating the image. This method is dormant 
        in v1.0. 
        @param kwargs A dictionary of parameters passed from the caller  to the instance. This method passes kwargs to the constructor of CovidDailyCases().
        """          
        covidDailyCases = CovidDailyCases(**kwargs)
        return covidDailyCases.getImage()

# SearchResults parts
class CovidContent(ABC):
    """!
    Abstract class for all classes that construct a representation of Covid data in a graphical and/or textual format
    """    
    def __init__(self, **kwargs):pass
    def getImage(self): pass
    def getMsgText(self): pass
    def isDataAvailable(self): pass

class CovidAggregateCasesDeceased(CovidContent):
    """!
    Constructs a graphic representing Aggregate proportions of COVID cases vs. deceased
    """
    def __init__(self, **kwargs):
        """! 
        Constuctor for the class. It accepts and saves the Request object passed via kwargs for later use. 
        @param kwargs A dictionary of parameters passed from the caller  to the instance. This method parses the parameter named REQUEST containing the Request from the dictionary. 
        """          
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None
    def isDataAvailable(self): pass

    def getinfo(self): pass

    def getImage(self):       
        """! 
        Using the Request.search_type() method defined on the instance Request object, this method performs a zipcode-based the search to retrieve data and generate graphs. It 
        creates a CovidModelFactory instance to retrieve Daily COVID data. The data retrieved is passed to a GraphicsFactory instance to generate a pie chart of cases vs. deceased aggregate totals.

        Parameters passed to instantiate other classes:
        1. Get data: CovidModelFactory(MODEL_TYPE=CovidModel.MONTHLY_CASES_DECEASED, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE=self.__requestObj.zip,ReturnType=DjangoDB.DICTIONARIES)
        2. Generat graph: CovidModelFactory(MODEL_TYPE=CovidModel.MONTHLY_CASES_DECEASED, LOCATION=CovidModel.LOCATION_COUNTY, COUNTY=self.__requestObj.county,ReturnType=DjangoDB.DICTIONARIES )
        
        @return Returns a byte stream of a png image. 
        """           
        imageStream = "data:image/png;base64,"
        try:
            if self.__requestObj.search_type() == Request.ZIPCODE:
                imageData = CovidModelFactory(MODEL_TYPE=CovidModel.AGGREGATE_CASES_DECEASED, LOCATION=CovidModel.LOCATION_ZIPCODE, 
                            ZIPCODE=self.__requestObj.zip,ReturnType=DjangoDB.DICTIONARIES )
            
            elif self.__requestObj.search_type() == Request.COUNTY_ONLY:
                imageData = CovidModelFactory(MODEL_TYPE=CovidModel.AGGREGATE_CASES_DECEASED, LOCATION=CovidModel.LOCATION_COUNTY,
                            COUNTY=self.__requestObj.county,ReturnType=DjangoDB.DICTIONARIES )
            else:
                print ("CovidAggregateCasesDeceased.getImage().1 - expected request type ZIPCODE or COUNTY in params - received:",self.__requestObj)
                return None
        except:
            print ("CovidAggregateCasesDeceased.getImage().2 - unexpected error: ",sys.exc_info()[0])
            return None            

        try:
            if imageData.DataAvailable:
                request_data = imageData.CovidData
            else:
                return None
                
            pieGraph = GraphicsFactory(GRAPHIC_TYPE=Graphic.PIE, IMAGE_DATA=request_data, LOCATION=self.__requestObj.zip)          
            imageStream+=pieGraph.image
            return imageStream

        except:
            print ("CovidAggregateCasesDeceased.getImage().3 - unexpected error: ",sys.exc_info()[0])
            return None   

class CovidMonthlyCasesDeceased(CovidContent):
    """!
    Constructs a graphic presenting monthly counts of COVID cases vs. deceased
    """
    def __init__(self, **kwargs):
        """! 
        Constuctor for the class. It accepts and saves the Request object passed via kwargs for later use. 
        @param kwargs A dictionary of parameters passed from the caller to the instance. This method parses the parameter named REQUEST containing the Request from the dictionary. 
        """          
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None

    def getinfo(self): pass
    
    def getImage(self):       
        """! 
        Using the Request.search_type() method defined on the instance Request object, this method performs a zipcode-based the search to retrieve data and generate graphs. It 
        creates a CovidModelFactory instance to retrieve Daily COVID data. The data retrieved is passed to a GraphicsFactory instance to generate a stackplot graph of cases vs. deceased monthly totals.

        Parameters passed to instantiate other classes:
        1. Get data: CovidModelFactory(MODEL_TYPE=CovidModel.MONTHLY_CASES_DECEASED, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE=self.__requestObj.zip,ReturnType=DjangoDB.DICTIONARIES)
        2. Generate graph: CovidModelFactory(MODEL_TYPE=CovidModel.MONTHLY_CASES_DECEASED, LOCATION=CovidModel.LOCATION_COUNTY, COUNTY=self.__requestObj.county,ReturnType=DjangoDB.DICTIONARIES )

        @return Returns a byte stream of a png image. 
        """           
        imageStream = "data:image/png;base64,"
        try:
            if self.__requestObj.search_type() == Request.ZIPCODE:
                imageData = CovidModelFactory(MODEL_TYPE=CovidModel.MONTHLY_CASES_DECEASED, LOCATION=CovidModel.LOCATION_ZIPCODE, 
                            ZIPCODE=self.__requestObj.zip,ReturnType=DjangoDB.DICTIONARIES)
            
            elif self.__requestObj.search_type() == Request.COUNTY_ONLY:
                imageData = CovidModelFactory(MODEL_TYPE=CovidModel.MONTHLY_CASES_DECEASED, LOCATION=CovidModel.LOCATION_COUNTY,
                            COUNTY=self.__requestObj.county,ReturnType=DjangoDB.DICTIONARIES )
            else:
                print ("CovidMonthlyCasesDeceased.getImage().1 - expected request type ZIPCODE or COUNTY in params - received:",self.__requestObj)
                return None
        except:
            print ("CovidMonthlyCasesDeceased.getImage().2 - unexpected error: ",sys.exc_info()[0])
            return None            

        try:
            if imageData.DataAvailable:
                request_data = imageData.CovidData
            else:
                return None
                
            chartGraph = GraphicsFactory(GRAPHIC_TYPE=Graphic.STACKPLOT, IMAGE_DATA=request_data)
            imageStream+=chartGraph.image
            return imageStream
        except:
            print ("CovidMonthlyCasesDeceased.getImage().3 - unexpected error: ",sys.exc_info()[0])
            return None   


class CovidDailyCases(CovidContent):
    """!
    Constructs a graphic presenting daily counts of COVID county vs. state cases and deceased 
    """
    def __init__(self, **kwargs):
        """! 
        Constuctor for the class. It accepts and saves the Request object passed via kwargs for later use. 
        @param kwargs A dictionary of parameters passed from the caller to the instance. This method parses the parameter named REQUEST containing the Request from the dictionary. 
        """             
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None
    
    def isDataAvailable(self): pass

    def getinfo(self): pass

    def getImage(self):       
        """! 
        Using the Request.search_type() method defined on the instance Request object, this method performs a zipcode-based the search to retrieve data and generate graphs. It 
        creates a CovidModelFactory instance to retrieve Daily COVID data. The data retrieved is passed to a GraphicsFactory instance to generate a dual plot graph of deceased county vs. state daily totals.

        Parameters passed to instantiate other classes:
        1. Locate state where zipcode located: CovidModelFactory(MODEL_TYPE=CovidModel.MESSAGES, ZIPCODE_STATE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES)
        2. Get county data: CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES)
        3. Get state data: CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, LOCATION=CovidModel.LOCATION_STATE, STATE=zip_state[0], ReturnType=DjangoDB.DICTIONARIES)
        4. Generate graph: GraphicsFactory(GRAPHIC_TYPE=Graphic.DUAL_PLOT, COUNTY_DATA=county_data, STATE_DATA=state_data, STATE=zip_state[0])
        
        @return Returns a list of two byte streams containing png image data. casesDailyGraph.image[0] returns the cases graph and casesDailyGraph.image returns the deceased graph. 
        """        
        # there are 3 queries to run: 
        # 1. get the state the zip code resides in (zipcode querying is the only search_type supported in v1.0)
        # 2. get the county level data for the zip code - this can result in multiple counties, for this release we only use the first county returned
        # 3. get the state level data for the zip code
        try:
            if self.__requestObj.search_type() == Request.ZIPCODE:
                
                #get state where zip code resides
                resultSet = CovidModelFactory(MODEL_TYPE=CovidModel.MESSAGES, ZIPCODE_STATE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES )
                if resultSet.DataAvailable:
                    zip_state = resultSet.CovidData
                else:
                    #print("CovidDailyCases.getImage().1 - no data returned for zipcode = ", self.__requestObj.zip)
                    self.__requestObj.setErrMsg("No data was available for zip code " + self.__requestObj.zip)
                    return None

                # get county data
                resultSet = CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, LOCATION=CovidModel.LOCATION_ZIPCODE, 
                                                ZIPCODE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES)
                if resultSet.DataAvailable:
                    county_data = resultSet.CovidData
                else:
                    print("CovidDailyCases.getImage().2 - no data returned for zipcode = ", self.__requestObj.zip)
                    return None          
                
                # get state data
                resultSet = CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, LOCATION=CovidModel.LOCATION_STATE,
                                                STATE=zip_state[0], ReturnType=DjangoDB.DICTIONARIES )
                if resultSet.DataAvailable:
                    state_data = resultSet.CovidData
                else:
                    print("CovidDailyCases.getImage().3 - no data returned for zipcode = ", self.__requestObj.zip)
                    return None

            else:
                print ("CovidDailyCases.getImage().4 - expected request type ZIPCODE in params - received:",self.__requestObj)
                return None
        except:
            print ("CovidDailyCases.getImage().5 - unexpected error: ",sys.exc_info()[0])
            return None            

        try:  # generate graph from data
            casesDailyGraph = GraphicsFactory(GRAPHIC_TYPE=Graphic.DUAL_PLOT, COUNTY_DATA=county_data, 
                                                STATE_DATA=state_data, STATE=zip_state[0])
            return casesDailyGraph.image
        
        except:
            print ("CovidDailyCases.getImage().3 - unexpected error: ",sys.exc_info()[0])
            return None   


class CovidDailyDeceased(CovidContent):
    """!
    Constructs a graphic presenting daily counts of COVID county vs. state deceased. This is dormant in v1.0 and will be active in v1.1. 
    """
    def __init__(self, **kwargs):
        """! 
        Constuctor for the class. It accepts and saves the Request object passed via kwargs for later use. 
        @param kwargs A dictionary of parameters passed from the caller to the instance. This method parses the parameter named REQUEST containing the Request from the dictionary. 
        """       
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None
    
    def isDataAvailable(self): pass

    def getinfo(self): pass

    def getImage(self):       
        """! 
        Using the Request.search_type() method defined on the instance Request object, this method performs zipcode-based search. It creates a CovidModelFactory instance to 
        retrieve Daily COVID data. The data retrieved is passed to a GraphicsFactory instance to generate a dual plot graph of deceased county vs. state daily totals.

        Parameters passed to instantiate other classes:
        1. Locate state where search zipcode is located: CovidModelFactory(MODEL_TYPE=CovidModel.MESSAGES, ZIPCODE_STATE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES)
        2. Get county data: CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES)
        3. Get state data: CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, LOCATION=CovidModel.LOCATION_STATE, STATE=zip_state[0], ReturnType=DjangoDB.DICTIONARIES)
        4. Generate graph: GraphicsFactory(GRAPHIC_TYPE=Graphic.DUAL_PLOT, COUNTY_DATA=county_data, STATE_DATA=state_data, STATE=zip_state[0])
        
        @return Returns a byte stream containing png image data for the dual plot  
        """        
        # there are 3 queries to run: 
        # 1. get the state the zip code resides in (zipcode querying is the only search_type supported in v1.0)
        # 2. get the county level data for the zip code - this can result in multiple counties, for this release we only use the first county returned
        # 3. get the state level data for the zip code
        try:
            if self.__requestObj.search_type() == Request.ZIPCODE:
                
                # get state where zip code resides
                resultSet = CovidModelFactory(MODEL_TYPE=CovidModel.MESSAGES, ZIPCODE_STATE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES )
                if resultSet.DataAvailable:
                    zip_state = resultSet.CovidData
                else:
                    print("CovidDailyCases.getImage().1 - no data returned for zipcode = ", self.__requestObj.zip)
                    return None

                # get county data
                resultSet = CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, LOCATION=CovidModel.LOCATION_ZIPCODE, 
                                                ZIPCODE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES)
                if resultSet.DataAvailable:
                    county_data = resultSet.CovidData
                else:
                    print("CovidDailyCases.getImage().2 - no data returned for zipcode = ", self.__requestObj.zip)
                    return None          
                
                # get state data
                resultSet = CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, LOCATION=CovidModel.LOCATION_STATE,
					                            STATE=zip_state[0], ReturnType=DjangoDB.DICTIONARIES )
                if resultSet.DataAvailable:
                    state_data = resultSet.CovidData
                else:
                    print("CovidDailyCases.getImage().3 - no data returned for zipcode = ", self.__requestObj.zip)
                    return None

            else:
                print ("CovidDailyCases.getImage().4 - expected request type ZIPCODE in params - received:",self.__requestObj)
                return None
        except:
            print ("CovidDailyCases.getImage().5 - unexpected error: ",sys.exc_info()[0])
            return None            

        try:  # generate graph from data
            deceasedDailyGraph = GraphicsFactory(GRAPHIC_TYPE=Graphic.DUAL_PLOT, COUNTY_DATA=county_data, STATE_DATA=state_data, STATE=zip_state[0])
            return deceasedDailyGraph.image
	
        except:
            print ("CovidDailyCases.getImage().3 - unexpected error: ",sys.exc_info()[0])
            return None   


class CovidInfoMsgs(CovidContent):
    """!
    Constructs info messages related to a Covid search
    """
    def __init__(self, **kwargs):
        """! 
        Constuctor for the class. It accepts and saves the Request object passed via kwargs for later use. 
        @param kwargs A dictionary of parameters passed from the caller to the instance. This method parses the parameter named REQUEST containing the Request from the dictionary. 
        """         
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None

    def isDataAvailable(self): pass

    def getImage(self): pass
	
    def getMsgText(self):
        """! 
        Retrieves any informational messages related to the search requested by the user. It creates an instance CovidModelFactory to retrieve messages for the 
        specific zipcode used for the search. It also performs a query to determine if the zip code appears in more than one county. Parameters are passed to the CovidModelFactory
        to instantiate objects that request the data.

        Parameters passed to invoke instantiate other classes:
        1. General info: CovidModelFactory(MODEL_TYPE=CovidModel.MESSAGES, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE=zip code, ReturnType=DjangoDB.DICTIONARIES)
        2. Multiple county info: CovidModelFactory(MODEL_TYPE=CovidModel.MESSAGES, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE_COUNTIES=zip code, ReturnType=DjangoDB.DICTIONARIES)

        @return Returns a list of informational messages related to the search location. 
        """  	      
        try:
            # msgs for zip    
            msg_text=''
            data = CovidModelFactory(MODEL_TYPE = CovidModel.MESSAGES, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES )
            if data.DataAvailable:
                msg_text = data.CovidData

            # multiple counties for zip
            data = CovidModelFactory(MODEL_TYPE = CovidModel.MESSAGES, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE_COUNTIES=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES )
            if data.DataAvailable:
                if len(data.CovidData) >1:
                    msg_text[0]+= " - " + str(data.CovidData).strip('[]')
            
            return str(msg_text).strip('[]')

        except:
            print ("CovidInfoMsgs.getMsgInfo().1 - unexpected error: ",sys.exc_info()[0])
            return msg_text 


class CovidLocation(CovidContent):
    """!
    Constructs and returns location info related to a Covid search.
    """
    def __init__(self, **kwargs):
        """! 
        Constuctor for the class. It accepts and saves the Request object passed via kwargs for later use. 
        @param kwargs A dictionary of parameters passed from the caller to the instance. This method parses the parameter named REQUEST containing the Request from the dictionary. 
        """         
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None

    def getImage(self): pass

    def getMsgText(self): pass

    def isDataAvailable(self):
        """! 
        Determines if there is any reportable data for the zipcode and returns either True/False. It constructs a CovidModelFactory object and passes a parameter list containing:
        MODEL_TYPE, LOCATION_TYPE, ZIPCODE and ReturnType.

        @return Returns a list of informational messages related to the search location. 
        """ 	    
        # determin if data available for request - currently only supports zip code test
        try:
            data = CovidModelFactory(MODEL_TYPE = CovidModel.LOCATIONS, LOCATION_TYPE=CovidLocationInfo.DATA_PRESENT_FOR_ZIP, ZIPCODE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES )
            if data.DataAvailable:
                return True
            else:
                return False		
        except:
            print ("CovidLocation.isDataAvailable() - unexpected error: ",sys.exc_info()[0])
            return False         
