"""! @brief COVID Traveler models package code"""

##
# @file models.py
#
# @brief models.py contains code that implements the models logic to access data on behalf of callers. With the exception of the Feedback class that uses the Django ORM for data access, all other model classes
# are implemented using a Factory design pattern that inherit from the abstract CovidModel class.
#
## @section description_models Description
# With the exception of the Feedback class which uses the Django ORM to access the database, all other classes inherit from CovidModel using a factory pattern. The factory class CovidModelFactory 
# uses a parameterized approach to select a concrete class to support a caller's request for model functionality. The factory class can delegate to five other classes depending upon
# the parameters passed:
# 1. CovidLocationInfo
# 2. CovidMessages
# 3. CovidAggregateTotals
# 4. CovidMonthlyTotals
# 5. CovidDailyTotals
#
## @section libraries_models Libraries/Modules
# - Django/Python imports:
#  - sys from python
#  - models from djangodb
#  - ABC, abstractmethod from abc
# - Application imports:
#   - DjangoDB, PersistanceRequest from pages.persistence
#
## @section author_models Author(s)
# - Created by Team #3 on 11/29/2020.
# - Modified by Team #3 on 11/29/2020.
#
# Copyright (c) 2020 COVID Traveler Warning Team.  All rights reserved.

from django.db import models
from pages.persistence import DjangoDB, PersistanceRequest
from abc import ABC, abstractmethod
import sys

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_feedback'


class CovidModel(ABC):

    AGGREGATE_CASES_DECEASED = 1
    MONTHLY_CASES_DECEASED = 2
    PAST_30_DAYS = 3
    LOCATION_ZIPCODE = 4
    LOCATION_COUNTY = 5
    LOCATION_STATE = 6
    LOCATIONS = 7
    MESSAGES = 8

    persist = DjangoDB()

    def __init__(self, *args, **kwargs):
        super().__init__()

    def getData(self, *args, **kwargs):
        raise NotImplementedError


class CovidModelFactory(CovidModel):
    """
    This concrete class uses a simple parameterized approach to constructing the required CovidData subclass
    needed by the consumer.
    """
    def __init__(self, *args, **kwargs):
        self.__createCovidModelInstance(*args, **kwargs)

    def __getData(self, *args, **kwargs):
        pass

    def __isDataAvailable(self, CovidData):
        """
        docstring
        """
        try:
            if self.CovidData != None:
                if self.CovidData == []:
                    return False          
                if self.CovidData == [None]:
                    return False
                else:               
                    if len(self.CovidData[0])>0:
                        return True                  
            else:
                return False
        except:
            print ("CovidMessages.__isDataAvailable() - unexpected error: ",sys.exc_info()[0])
            return False    

    
    def __createCovidModelInstance(self, *args, **kwargs):
        """
        Use the args to identify the appropriate model class
        """
        try:
            if 'MODEL_TYPE' in kwargs:
                if kwargs['MODEL_TYPE'] == CovidModel.AGGREGATE_CASES_DECEASED:
                    covidModel = CovidAggregateTotals()                   
                    self.CovidData = covidModel.getData(*args,**kwargs)
                    self.DataAvailable=self.__isDataAvailable(self.CovidData)
                    return 
                    
                if kwargs['MODEL_TYPE'] == CovidModel.MONTHLY_CASES_DECEASED:
                    covidModel = CovidMonthlyTotals()                   
                    self.CovidData = covidModel.getData(*args,**kwargs)
                    self.DataAvailable=self.__isDataAvailable(self.CovidData)
                    return                     

                if kwargs['MODEL_TYPE'] == CovidModel.PAST_30_DAYS:
                    covidModel = CovidDailyTotals()                   
                    self.CovidData = covidModel.getData(*args,**kwargs)
                    self.DataAvailable=self.__isDataAvailable(self.CovidData)
                    return 

                if kwargs['MODEL_TYPE'] == CovidModel.MESSAGES:
                    covidModel = CovidMessages()                   
                    self.CovidData = covidModel.getData(*args,**kwargs)
                    self.DataAvailable=self.__isDataAvailable(self.CovidData)
                    return

                if kwargs['MODEL_TYPE'] == CovidModel.LOCATIONS:
                    covidModel = CovidLocationInfo()                   
                    self.CovidData = covidModel.getData(*args,**kwargs)
                    self.DataAvailable=self.__isDataAvailable(self.CovidData)
                    return

            print ("CovidMessages.__createCovidModelInstance() - did not receive a recognizable model type - no model object instantiated. Args received = ",kwargs)
            return None
        except:
            print ("CovidMessages.__createCovidModelInstance() - unexpected error: ",sys.exc_info()[0])
            return None    

class CovidLocationInfo(CovidModel):
    """
    Note - all SQLs must return a column named 'Location' for this class to return a result. That column will contain the text that will be returned to the caller.
    """
    __argList = []
    __argDict = {} 
    __sql = ''
    __data = None 

    COUNTIES_BY_ZIP = 1
    ZIP_IN_STATES = 2
    UNIQUE_STATE = 3
    COUNTIES_IN_STATE = 4
    DATA_PRESENT_FOR_ZIP = 5

    __sqlDataExistsForZip="""
    SELECT cast(max(last_update) as char) as Location
    FROM covidtraveler_db.covid_finalmaster_table
    WHERE fips in (SELECT uzf.STcountyFIPS 
				    FROM covidtraveler_db.US_ZIP_FIPS uzf
                    WHERE uzf.zip = %s);
    """ 

    __sqlCountiesForZip="""
    SELECT distinct CountyName as Location FROM covidtraveler_db.US_ZIP_FIPS
    where zip = %s;
    """ 
    
    __sqlZipState="""
    SELECT distinctrow uzf.zip , sn.state_fullname as Location
    FROM covidtraveler_db.US_ZIP_FIPS uzf
    inner join covidtraveler_db.fips_county_state_names sn
    on sn.fips = uzf.STcountyFIPS
    where uzf.zip = %s
    order by uzf.State;
    """

    __sqlAllStates="""
    SELECT distinct state_fullname as Location
    FROM covidtraveler_db.state_name_xref
    order by state_fullname;
    """

    __sqlCountiesInState="""
    SELECT county_basename as Location
    FROM covidtraveler_db.fips_county_state_names
    WHERE state_fullname = %s;
    """

    def __init__(self, *args, **kwargs):
        super().__init__()
 
        __argList=args
        __argDict=kwargs   
              
    def __getData(self, *args, **kwargs):
        try:
            self.dbReq = PersistanceRequest(ReturnType=kwargs['ReturnType'], SQL=self.__sql, whereParams=self.__data)
            return CovidModel.persist.getData(self.dbReq)

        except:
            print ("CovidLocationInfo.__getData() - unexpected error: ",sys.exc_info()[0])
            return None        

    def getData(self, *args, **kwargs):
        try:
            if 'LOCATION_TYPE' in kwargs:
                if kwargs['LOCATION_TYPE'] == CovidLocationInfo.COUNTIES_BY_ZIP: 
                    self.__sql = CovidLocationInfo.__sqlCountiesForZip
                    self.__data=[kwargs['ZIPCODE']]

                elif kwargs['LOCATION_TYPE'] == CovidLocationInfo.ZIP_IN_STATES: 
                    self.__sql = CovidLocationInfo.__sqlZipState
                    self.__data=[kwargs['ZIPCODE_COUNTIES']]

                elif kwargs['LOCATION_TYPE'] == CovidLocationInfo.UNIQUE_STATE: 
                    self.__sql=CovidLocationInfo.__sqlAllStates
                    self.__data=None

                elif kwargs['LOCATION_TYPE'] == CovidLocationInfo.COUNTIES_IN_STATE: 
                    self.__sql=CovidLocationInfo.__sqlCountiesInState
                    self.__data=[kwargs['ZIPCODE_STATE']]

                elif kwargs['LOCATION_TYPE'] == CovidLocationInfo.DATA_PRESENT_FOR_ZIP: 
                    self.__sql=CovidLocationInfo.__sqlDataExistsForZip
                    self.__data=[kwargs['ZIPCODE']]
            else:
                print ("CovidLocationInfo.getData() - missing expected key LOCATION_TYPE in argument list - received: ",kwargs)
                return None
            
            self.result = self.__getData(SQL=self.__sql, whereParams=self.__data, **kwargs)
            self.__msg = [d.get('Location', None) for d in self.result]

            if self.__msg != None:
                return self.__msg
            else:
                return None
        except:
            print ("CovidLocationInfo.getData() - unexpected error: ",sys.exc_info()[0])
            return None


class CovidMessages(CovidModel):
    """
    Note - all SQLs must return a column named 'msg_text' for this class to return a result. That column will contain the text that will be returned for display
    """
    __argList = []
    __argDict = {} 
    __sql = ''
    __data = None 

    def __init__(self, *args, **kwargs):
        super().__init__()
 
        __argList=args
        __argDict=kwargs   
              
        self._sqlZipMsgs_="""
		select distinctrow zm.zipcode, mt.msg_text 
		from zips_msgs zm
		inner join msg_text mt on zm.msg_id = mt.msg_id
		where zm.zipcode = %s;
		"""

       	self._sqlCountyMsgs_="""
		select fc.county_name, fc.fips, mt.msg_text 
		from fips_county fc
		inner join fips_msgs fm on fm.fips = fc.fips
		inner join msg_text mt on mt.msg_id = fm.msg_id
		where fc.county_name = %s
		"""
        
        self._sqlZipCounties_="""
        SELECT distinct CountyName as msg_text FROM covidtraveler_db.US_ZIP_FIPS
        where zip = %s;
        """ 
        
        self._sqlZipState_="""
        SELECT distinctrow uzf.zip , sn.state_fullname as msg_text
        FROM covidtraveler_db.US_ZIP_FIPS uzf
        inner join covidtraveler_db.fips_county_state_names sn
        on sn.fips = uzf.STcountyFIPS
        where uzf.zip = %s
        order by uzf.State;
        """

    def __getData(self, *args, **kwargs):
        try:
            self.dbReq = PersistanceRequest(ReturnType=kwargs['ReturnType'], SQL=self.__sql, whereParams=self.__data)
            return CovidModel.persist.getData(self.dbReq)

        except:
            print ("CovidMessages._getData_() - unexpected error: ",sys.exc_info()[0])
            return None        

    def getData(self, *args, **kwargs):
        try:
            if 'ZIPCODE' in kwargs:                
                self.__sql=self._sqlZipMsgs_
                self.__data=[kwargs['ZIPCODE']]
    
            elif 'STATE' in kwargs and 'COUNTY' in kwargs: #only interested in case where both are populated
                self.__sql=self._sqlCountyMsgs_
                self.__data=[kwargs['STATE'],kwargs['COUNTY']]

            elif 'ZIPCODE_COUNTIES' in kwargs: 
                self.__sql=self._sqlZipCounties_
                self.__data=[kwargs['ZIPCODE_COUNTIES']]

            elif 'ZIPCODE_STATE' in kwargs: 
                self.__sql=self._sqlZipState_
                self.__data=[kwargs['ZIPCODE_STATE']]

            else:
                print ("CovidMessages.getData() - missing expected keys ZIPCODE or STATE/COUNTY combination in argument list - received: ",kwargs)
                return None
            
            self.result = self.__getData(SQL=self.__sql, whereParams=self.__data, **kwargs)
            self.__msg = [d.get('msg_text', None) for d in self.result]

            if self.__msg != None:
                return self.__msg
            else:
                return None
        except:
            print ("CovidMessages.getData() - unexpected error: ",sys.exc_info()[0])
            return None

class CovidAggregateTotals(CovidModel):
    __sql = ''
    __data = None

    __sqlZipTotals= """
        SELECT uzf.STcountyFIPS AS FIPS, cft.county AS County, cft.province_state AS State,
        SUM(cft.daily_confirmed_case) AS Cases, SUM(cft.daily_deaths_case) AS Deceased 
        FROM covid_finalmaster_table cft JOIN US_ZIP_FIPS uzf ON ((cft.FIPS = uzf.STcountyFIPS)) 
        WHERE uzf.zip = %s 
        GROUP BY uzf.STcountyFIPS , cft.county , cft.province_state 
        """
    __sqlStateCountyTotals = """
        SELECT uzf.STcountyFIPS AS FIPS, cft.county AS County, cft.province_state AS State,
        SUM(cft.daily_confirmed_case) AS Cases, SUM(cft.daily_deaths_case) AS Deceased
        FROM covid_finalmaster_table cft JOIN US_ZIP_FIPS uzf ON ((cft.FIPS = uzf.STcountyFIPS))
        WHERE uzf.CountyName = %s
        and uzf.State = %s
        GROUP BY uzf.STcountyFIPS , cft.county , cft.province_state;
        """
    def __init__(self, *args, **kwargs):
        super().__init__()

    def getData(self, *args, **kwargs):
        """
        docstring
        """
        return self.__getData(self, *args, **kwargs)

    def __getData(self, *args, **kwargs):
        """
        docstring
        """        
        try:
            #print("CovidAggregateTotals __getData()  kwargs=", kwargs)
            if 'LOCATION' in kwargs:
                
                if kwargs['LOCATION']==CovidModel.LOCATION_ZIPCODE:
                    self.__sql = self.__sqlZipTotals
                    self.__data = [kwargs['ZIPCODE']]
                
                elif kwargs['LOCATION']==CovidModel.LOCATION_COUNTY:
                    self.__sql = self.__sqlStateCountyTotals
                    self.__data = [kwargs['STATE'],kwargs['COUNTY']]

                if 'ReturnType' in kwargs:
                    retType=kwargs['ReturnType']

                self.dbReq = PersistanceRequest(ReturnType=retType, SQL=self.__sql, whereParams=self.__data)

                return CovidModel.persist.getData(self.dbReq)            
            else:
                print ("CovidAggregateTotals.__getData() - LOCATION param not provided, received: ", kwargs)
                return None       
            return None
        except:
            print ("CovidAggregateTotals.__getData() - unexpected error: ",sys.exc_info()[0])
            return None        
        
class CovidMonthlyTotals(CovidModel):
    __sql = ''
    __data = None

    __sqlZipTotals = """
        SELECT monthname(cft.last_update) as Month_part, STcountyFIPS as FIPS, cft.county,  cft.province_state as state, cft.confirmed as Cases, cft.deaths as Deceased
        FROM covidtraveler_db.covid_finalmaster_table cft inner join covidtraveler_db.US_ZIP_FIPS uzf
        on cft.FIPS = uzf.STcountyFIPS
        where dayofmonth(cft.last_update)=1
        and uzf.zip = %s
        order by STcountyFIPS, cft.last_update; 
        """
    __sqlStateCountyTotals = """
        SELECT monthname(cft.last_update) as Month_part, cft.FIPS, cft.county,  cft.province_state as state, cft.confirmed as Cases, cft.deaths as Deceased
        FROM covidtraveler_db.covid_finalmaster_table cft 
        where dayofmonth(cft.last_update)=1
        and cft.county = %s
        and cft.province_state = %s
        order by cft.FIPS, cft.last_update; 
        """
    def __init__(self, *args, **kwargs):
        super().__init__()

    def getData(self, *args, **kwargs):
        """
        docstring
        """
        #print("CovidMonthlyTotals getData()  kwargs=", kwargs)
        return self.__getData(self, *args, **kwargs)

    def __getData(self, *args, **kwargs):
        try:
            #print("CovidMonthlyTotals __getData()  kwargs=", kwargs)
            if 'LOCATION' in kwargs:
                
                if kwargs['LOCATION']==CovidModel.LOCATION_ZIPCODE:
                    self.__sql = self.__sqlZipTotals
                    self.__data = [kwargs['ZIPCODE']]
                
                elif kwargs['LOCATION']==CovidModel.LOCATION_COUNTY:
                    self.__sql = self.__sqlStateCountyTotals
                    self.__data = [kwargs['STATE'],kwargs['COUNTY']]

                elif kwargs['LOCATION']==CovidModel.LOCATION_COUNTY:
                    self.__sql = self.__sqlStateCountyTotals
                    self.__data = [kwargs['STATE'],kwargs['COUNTY']]
                    
                if 'ReturnType' in kwargs:
                    retType=kwargs['ReturnType']

                self.dbReq = PersistanceRequest(ReturnType=retType, SQL=self.__sql, whereParams=self.__data)

                return CovidModel.persist.getData(self.dbReq)            
            else:
                print ("CovidMonthlyTotals.__getData() - LOCATION param not provided, received: ", kwargs)
                return None       
            return None
        except:
            print ("CovidMonthlyTotals.__getData() - unexpected error: ",sys.exc_info()[0])
            return None  
 
class CovidDailyTotals(CovidModel):
    __sql = ''
    __data = None

    __sqlZipTotals = """
        SELECT cft.province_state as state, cft.FIPS, cft.county, cft.last_update as event_day, 
            cft.daily_confirmed_case as Cases, cft.daily_deaths_case as Deceased
        FROM covidtraveler_db.covid_finalmaster_table cft inner join covidtraveler_db.US_ZIP_FIPS uzf
        ON cft.FIPS = uzf.STcountyFIPS
        where cft.last_update between date_sub(curdate(), INTERVAL 30 DAY) and curdate()
        and uzf.zip = %s
        order by cft.FIPS, cft.last_update;
        """

    __sqlStateCountyTotals = """
        SELECT cft.province_state as state, cft.FIPS, cft.county, cft.last_update as event_day, 
            cft.daily_confirmed_case as Cases, cft.daily_deaths_case as Deceased
        FROM covidtraveler_db.covid_finalmaster_table cft 
        WHERE cft.province_state = %s
        and cft.county = %s
        order by cft.FIPS, cft.last_update;        
        """

    __sqlStateOnlyTotals = """
 		SELECT cft.province_state as state, cft.last_update as event_day, sum(cft.daily_confirmed_case) as Cases, sum(cft.daily_deaths_case) as Deceased
		FROM covidtraveler_db.covid_finalmaster_table cft 
		where cft.last_update between date_sub(curdate(), INTERVAL 30 DAY) and curdate()
		and cft.province_state = %s
		group by cft.province_state, cft.last_update;
        """

    __sqlStateByZipTotals = """
 		SELECT cft.province_state as state, cft.last_update as event_day, sum(cft.daily_confirmed_case) as Cases, sum(cft.daily_deaths_case) as Deceased
		FROM covidtraveler_db.covid_finalmaster_table cft 
		where cft.last_update between date_sub(curdate(), INTERVAL 30 DAY) and curdate()
		and cft.province_state = %s
		group by cft.province_state, cft.last_update;
        """

    def __init__(self, *args, **kwargs):
        super().__init__()

    def getData(self, *args, **kwargs):
        """
        docstring
        """
        #print("CovidMonthlyTotals getData()  kwargs=", kwargs)
        return self.__getData(self, *args, **kwargs)

    def __getData(self, *args, **kwargs):
        try:
            #print("CovidMonthlyTotals __getData()  kwargs=", kwargs)
            if 'LOCATION' in kwargs:
                
                if kwargs['LOCATION']==CovidModel.LOCATION_ZIPCODE:
                    self.__sql = self.__sqlZipTotals
                    self.__data = [kwargs['ZIPCODE']]
                
                elif kwargs['LOCATION']==CovidModel.LOCATION_COUNTY:
                    self.__sql = self.__sqlStateCountyTotals
                    self.__data = [kwargs['STATE'],kwargs['COUNTY']]

                elif kwargs['LOCATION']==CovidModel.LOCATION_STATE:
                    self.__sql = self.__sqlStateOnlyTotals
                    self.__data = [kwargs['STATE']]                
                    
                if 'ReturnType' in kwargs:
                    retType=kwargs['ReturnType']

                self.dbReq = PersistanceRequest(ReturnType=retType, SQL=self.__sql, whereParams=self.__data)

                return CovidModel.persist.getData(self.dbReq)            
            else:
                print ("CovidMonthlyTotals.__getData() - LOCATION param not provided, received: ", kwargs)
                return None       
            return None
        except:
            print ("CovidMonthlyTotals.__getData() - unexpected error: ",sys.exc_info()[0])
            return None 
