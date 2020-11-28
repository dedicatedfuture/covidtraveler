# builder.py contains classes that direct the construction of web page objects that 
# are requested by the user.

import sys
from abc import ABC, abstractmethod
from pages.request import Request
from pages.models import CovidMessages, CovidModelFactory, CovidModel, CovidLocationInfo
from pages.persistence import DjangoDB
from pages.graphics import GraphicsFactory, Graphic
from django.shortcuts import render
from django.http import HttpResponse, HttpRequest


# Using the Builder design pattern, the Director class manages construction of the SearchResults
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

        # test for data available - if not, exit early and provide error text
        if self.__builder.isDataAvailableForRequest(REQUEST=self.__request) == False:
            self.__request.setErrMsg("No data was returned for zip code " + self.__request.zip)
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

        return searchResults.getSearchContext()

        # the search results page always expects 4 graphs, but info messages aren't always generated


class Builder:
    def isDataAvailableForRequest(self, **kwargs) : pass
    def getCovidAggregateCasesDeceased(self, **kwargs): pass
    def getCovidMonthlyCasesDeceased(self, **kwargs): pass
    def getCovidDailyCases(self, **kwargs): pass
    def getCovidDailyDeceased(self, **kwargs): pass
    def getCovidInfoMsgs(self, **kwargs): pass

class SearchResults:
    context = {}

    def __init__(self):
        SearchResults.context = {}
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

    def isDataAvailableForRequest(self, **kwargs):
        print("CovidLocation created") 
        dataAvailable = CovidLocation(**kwargs)
        return dataAvailable.isDataAvailableForZip()
    
    def getCovidInfoMsgs(self, **kwargs): 
        print("CovidInfoMsgs created") 
        getCovidInfoMsgs = CovidInfoMsgs(**kwargs)
        return getCovidInfoMsgs.getMsgInfo()

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
    Constructs a graphic presenting daily counts of COVID county vs. state cases and deceased 
    """
    def __init__(self, **kwargs):
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None
    
    def getImage(self):       
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
            casesDailyGraph = GraphicsFactory(GRAPHIC_TYPE=Graphic.DUAL_PLOT, COUNTY_DATA=county_data, STATE_DATA=state_data, STATE=zip_state[0])
            if casesDailyGraph.ImageAvailable:
                return casesDailyGraph.image
            else:
                print ("CovidDailyCases.getImage().5 - no image returned for zipcode = ", self.__requestObj.zip)
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

    def getImage(self):       
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
            casesDailyGraph = GraphicsFactory(GRAPHIC_TYPE=Graphic.DUAL_PLOT, COUNTY_DATA=county_data, STATE_DATA=state_data, STATE=zip_state[0])
            if casesDailyGraph.ImageAvailable:
                return casesDailyGraph.image
            else:
                print ("CovidDailyCases.getImage().5 - no image returned for zipcode = ", self.__requestObj.zip)
                err_msg = 'No data found for zipcode ' + self.__requestObj.zip 
                context = {'err_msg': err_msg}
                return render(self.__requestObj.request, 'pages/errorpage.html', context)	
	
        except:
            print ("CovidDailyCases.getImage().3 - unexpected error: ",sys.exc_info()[0])
            return None   


class CovidInfoMsgs:
    """
    Constructs info messages related to a Covid search
    """
    def __init__(self, **kwargs):
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None

    def getMsgInfo(self):
	    # msgs for zip
        try:
            msg_text=''
            data = CovidModelFactory(MODEL_TYPE = CovidModel.MESSAGES, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES )
            if data.DataAvailable:
                msg_text = data.CovidData
                #print ("CovidInfoMsgs.getMsgInfo().1 msg_text=",msg_text)		

            # multiple counties for zip
            data = CovidModelFactory(MODEL_TYPE = CovidModel.MESSAGES, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE_COUNTIES=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES )
            if data.DataAvailable:
                if len(data.CovidData) >1:
                    #print ("CovidInfoMsgs.getMsgInfo().2 data.CovidData=",data.CovidData)
                    msg_text[0]+= " - " + str(data.CovidData).strip('[]')
            
            return str(msg_text).strip('[]')

        except:
            print ("CovidInfoMsgs.getMsgInfo().1 - unexpected error: ",sys.exc_info()[0])
            return msg_text 


class CovidLocation:
    """
    Constructs location info related to a Covid search
    """
    def __init__(self, **kwargs):
        if 'REQUEST' in kwargs:
            self.__requestObj = kwargs['REQUEST']
        else:
            return None

    def isDataAvailableForZip(self):
	    # determin if data available for request - currently only supports zip code test
        try:
            #data = CovidModelFactory(MODEL_TYPE = CovidModel.LOCATIONS, LOCATION=CovidLocation.DATA_PRESENT_FOR_ZIP, ZIPCODE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES )
            data = CovidModelFactory(MODEL_TYPE = CovidModel.LOCATIONS, LOCATION_TYPE=CovidLocationInfo.DATA_PRESENT_FOR_ZIP, ZIPCODE=self.__requestObj.zip, ReturnType=DjangoDB.DICTIONARIES )
            if data.DataAvailable:
                return True
            else:
                return False		
        except:
            print ("CovidLocation.isDataAvailable() - unexpected error: ",sys.exc_info()[0])
            return False         
