# builder.py contains classes that direct the construction of web page objects that 
# are requested by the user.

import sys
from abc import ABC, abstractmethod
from pages.request import Request
from pages.models import CovidMessages, CovidModelFactory, CovidModel
from pages.persistence import DjangoDB
from pages.graphics import GraphicsFactory, Graphic
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


# the class that directs the construction of a RequestResponse
class Director:

    __builder = None

    def setBuilder(self, builder):
        self.__builder = builder

    def getSearchResults(self, *args, **kwargs):
        if 'REQUEST' in kwargs:
            self.__request = kwargs['REQUEST']
        else:
            self.__request = None        
            
        searchResults = SearchResults()

        # get aggregate graph
        aggGraph = self.__builder.getCovidAggregateCasesDeceased(REQUEST=self.__request)
        searchResults.setAggregateCovid(aggGraph)
        SearchResults.context['graph1']=aggGraph

        #get monthly graph
        monthlyGraph = self.__builder.getCovidMonthlyCasesDeceased(REQUEST=self.__request)
        searchResults.setMonthlyCovid(monthlyGraph)
        SearchResults.context['graph2']=monthlyGraph
        
        #get daily cases graph
        dailyCasesGraph = self.__builder.getCovidDailyCases(REQUEST=self.__request)
        searchResults.setDailyCases(dailyCasesGraph)
        SearchResults.context['graph3']=dailyCasesGraph

        #get daily deceased graph
        dailyDeceasedGraph = self.__builder.getCovidDailyDeceased(REQUEST=self.__request)
        searchResults.setDailyDeceased(dailyDeceasedGraph)
        SearchResults.context['graph4']=dailyDeceasedGraph

        #get info messages
        covidInfoMsgs = self.__builder.getCovidInfoMsgs(REQUEST=self.__request)
        searchResults.setCovidInfoMsgs(covidInfoMsgs)
        # create the msg_text dictionary element only if there is text present
        if len(covidInfoMsgs)>0:
            SearchResults.context['msg_text']=covidInfoMsgs

        return searchResults.getSearchContext()

        # the search results page always expects 4 graphs, but info messages aren't always generated


class Builder:
    def getCovidAggregateCasesDeceased(self, **kwargs): pass
    def getCovidMonthlyCasesDeceased(self, **kwargs): pass
    def getCovidDailyDeceased(self, **kwargs): pass
    def getCovidInfoMsgs(self, **kwargs): pass

class SearchResults:
    context = {}

    def __init__(self):
        self.__aggregateCovid = None
        self.__monthlyCovid = None
        self.__dailyCases = None
        self.__dailyDeceased = None
        self.__covidInfoMsgs = None
 
    def setAggregateCovid(self, aggGraph):
        self.__aggregateCovid = aggGraph

    def setMonthlyCovid(self, monthlyGraph):
        self.__monthlyCovid = monthlyGraph

    def setDailyCases(self, dailyCasesGraph):
        self.__dailyCases = dailyCasesGraph
    
    def setDailyDeceased(self, dailyDeceasedGraph):
        self.__dailyDeceased = dailyDeceasedGraph

    def setCovidInfoMsgs(self, covidInfoMsgs):
        self.__covidInfoMsgs = covidInfoMsgs

    def getSearchContext(self):
        return SearchResults.context


class SearchResultsBuilder(Builder):
    context = {}

    requestObj = None

    def __init__(self, *args, **kwargs):
        print("SearchResultsBuilder created")
        if 'REQUEST' in kwargs:
            self.__request = kwargs['REQUEST']
        else:
            self.__request = None

    def getCovidAggregateCasesDeceased(self, **kwargs): 
        print("CovidAggregateCasesDeceased created")
        covidAggregate = CovidAggregateCasesDeceased(**kwargs)
        return covidAggregate.getImage()        

    def getCovidMonthlyCasesDeceased(self, **kwargs): 
        print("CovidMonthlyCasesDeceased created") 
        covidMonthly = CovidMonthlyCasesDeceased(**kwargs)
        return covidMonthly.getImage()

    def getCovidDailyDeceased(self, **kwargs): 
        print("CovidDailyDeceased created")         
        covidDailyDeceased = CovidDailyDeceased(**kwargs)
        return covidDailyDeceased.getImage()

    def getCovidDailyCases(self, **kwargs): 
        print("CovidDailyCases created")         
        covidDailyCases = CovidDailyCases(**kwargs)
        return covidDailyCases.getImage()

    def getCovidInfoMsgs(self, **kwargs): 
        getCovidInfoMsgs = CovidInfoMsgs(**kwargs)
        print("CovidInfoMsgs created") 

# SearchResults parts

class CovidAggregateCasesDeceased:
    """
    Constructs a graphic presenting aggregate proportions of COVID cases vs. deceased
    """
    def __init__(self, **kwargs):
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None

    def getImage(self):       
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
                
            pieGraph = GraphicsFactory(GRAPHIC_TYPE=Graphic.PIE, IMAGE_DATA=request_data)
            
            if pieGraph!=None:
                imageStream+=pieGraph.image
                return imageStream
            else:	#populate error page
                err_msg = 'No data found for zipcode ' + self.__requestObj.zip 
                context = {'err_msg': err_msg}
                return render(self.__requestObj.request, 'pages/errorpage.html', context)	
        except:
            print ("CovidAggregateCasesDeceased.getImage().3 - unexpected error: ",sys.exc_info()[0])
            return None   

class CovidMonthlyCasesDeceased:
    """
    Constructs a graphic presenting monthly counts of COVID cases vs. deceased
    """
    def __init__(self, **kwargs):
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None
    
    def getImage(self):       
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
            
            if chartGraph!=None:
                imageStream+=chartGraph.image
                return imageStream
            else:	#populate error page
                err_msg = 'No data found for zipcode ' + self.__requestObj.zip 
                context = {'err_msg': err_msg}
                return render(self.__requestObj.request, 'pages/errorpage.html', context)	
        except:
            print ("CovidMonthlyCasesDeceased.getImage().3 - unexpected error: ",sys.exc_info()[0])
            return None   


class CovidDailyCases:
    """
    Constructs a graphic presenting daily counts of COVID county vs. state cases 
    """
    def __init__(self, **kwargs):
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None
    
    def getImage(self):       
        imageStream = "data:image/png;base64,"

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
                    print("CovidDailyCases.getImage().1 - no data returned for zipcode = ", self.__requestObj.zip)
                    return None                
                

                imageData = CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, LOCATION=CovidModel.LOCATION_ZIPCODE, 
                            ZIPCODE=self.__requestObj.zip,ReturnType=DjangoDB.DICTIONARIES)
           
           CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, 
				LOCATION=CovidModel.LOCATION_ZIPCODE, 
				ZIPCODE=req.zip, ReturnType=DjangoDB.DICTIONARIES )

            else:
                print ("CovidDailyCases.getImage().1 - expected request type ZIPCODE or COUNTY in params - received:",self.__requestObj)
                return None
        except:
            print ("CovidDailyCases.getImage().2 - unexpected error: ",sys.exc_info()[0])
            return None            

        try:
            if imageData.DataAvailable:
                request_data = imageData.CovidData
            else:
                return None
                
            casesDailyGraph = GraphicsFactory(GRAPHIC_TYPE=Graphic.DUAL_PLOT, IMAGE_DATA=request_data)
            
            if casesDailyGraph!=None:
                imageStream+=casesDailyGraph.image
                return imageStream
            else:	#populate error page
                err_msg = 'No data found for zipcode ' + self.__requestObj.zip 
                context = {'err_msg': err_msg}
                return render(self.__requestObj.request, 'pages/errorpage.html', context)	
        except:
            print ("CovidDailyCases.getImage().3 - unexpected error: ",sys.exc_info()[0])
            return None   


class CovidDailyDeceased:
    """
    Constructs a graphic presenting daily counts of COVID county vs. state deceased 
    """
    def __init__(self, **kwargs):
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None

class CovidInfoMsgs:
    """
    Constructs text related to a Covid search
    """
    def __init__(self, **kwargs):
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None