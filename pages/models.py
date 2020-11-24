from django.db import models
from . persistence import DjangoDB, PersistanceRequest
from abc import ABC, abstractmethod
import sys

class UsZipFips(models.Model):
    ziptable_id = models.AutoField(db_column='ZipTable_id', unique=True,primary_key=True)  # Field name made lowercase.
    zip = models.CharField(max_length=255, blank=True, null=True)
    countyname = models.CharField(db_column='CountyName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stcountyfips = models.CharField(db_column='STcountyFIPS', max_length=255, blank=True, null=True)  # Field name made lowercase.
 
    class Meta:
        managed = False
        db_table = 'US_ZIP_FIPS'

class CovidFinalmasterTable(models.Model):
    id = models.AutoField(unique=True,primary_key=True)
    fips = models.CharField(db_column='FIPS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    county = models.CharField(max_length=255, blank=True, null=True)
    province_state = models.CharField(max_length=255, blank=True, null=True)
    country_region = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long_field = models.FloatField(db_column='long_', blank=True, null=True)  # Field renamed because it ended with '_'.
    confirmed = models.FloatField(blank=True, null=True)
    deaths = models.FloatField(blank=True, null=True)
    recovered = models.FloatField(blank=True, null=True)
    active_case = models.FloatField(blank=True, null=True)
    daily_confirmed_case = models.FloatField(blank=True, null=True)
    daily_deaths_case = models.FloatField(blank=True, null=True)
 
    class Meta:
        managed = False
        db_table = 'covid_finalmaster_table'
    
    def __str__(self):
        return self.fips

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_feedback'


class CovidModel(ABC):

    TO_DATE_TOTALS_CASES_DECEASED = 1
    MONTHLY_TOTALS_CASES_DECEASED = 2
    PAST_30_DAYS_CASES = 3
    PAST_30_DAYS_DECEASED = 4
    LOCATION_ZIPCODE = 5
    LOCATION_COUNTY = 6

    persist = DjangoDB()

    def __init__(self, *args, **kwargs):
        super().__init__()

    def __getData(self, *args, **kwargs):
        raise NotImplementedError


class CovidMessages(CovidModel):
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

    def __getData(self, *args, **kwargs):
        try:
            self.dbReq = PersistanceRequest(ReturnType=DjangoDB.DICTIONARIES, SQL=kwargs['SQL'], whereParams=[kwargs['whereParams']])
            return self.persist.getData(self.dbReq)
        except:
            print ("CovidMessages._getData_() - unexpected error: ",sys.exc_info()[0])
            return None        
        
    def dataAvailableForRequest(self, *args, **kwargs):
        pass

    def getMessages(self, *args, **kwargs):
        try:
            if 'ZIPCODE' in kwargs:                
                self.__sql=self._sqlZipMsgs_
                self.__data=[kwargs['ZIPCODE']]
    
            elif 'STATE' in kwargs and 'COUNTY' in kwargs: #only interested in case where both are populated
                self.__sql=self._sqlCountyMsgs_
                self.__data=[kwargs['STATE'],kwargs['COUNTY']]
            
            else:
                print ("CovidMessages.getMessages() - missing expected keys ZIPCODE or STATE/COUNTY combination in argument list - received: ",kwargs)
                return None
            
            self.result = self.__getData(SQL=self.__sql, whereParams=self.__data)
            self.__msg = [d.get('msg_text', None) for d in self.result]

            if self.__msg != None:
                return self.__msg
            else:
                return None
        except:
            print ("CovidMessages.getMessages() - unexpected error: ",sys.exc_info()[0])
            return None

class CovidDataFactory(CovidModel):
    """
    This concrete class uses a simple parameterized approach to constructing the required CovidData subclass
    needed by the consumer.
    """
    def __init__(self, *args, **kwargs):
        self.__createCovidClassInstance(*args, **kwargs)

    def __getData(self, *args, **kwargs):
        pass

    def __createCovidClassInstance(self, *args, **kwargs):
        """
        Use the args to identify the ideal class
        """
        try:
            if 'MODEL_TYPE' in kwargs:
                if kwargs['MODEL_TYPE'] == CovidModel.TO_DATE_TOTALS_CASES_DECEASED:
                    covidModel = CovidTotalsToDate()                   
                    self.result = covidModel.getData(*args,**kwargs)
                    return self.result
                    
                if kwargs['MODEL_TYPE'] == CovidModel.MONTHLY_TOTALS_CASES_DECEASED:
                    print ("CovidDataFactory._createCovidClassInstance_() MONTHLY_TOTALS_CASES_DECEASED report selected")

                if kwargs['MODEL_TYPE'] == CovidModel.PAST_30_DAYS_CASES:
                    print ("CovidDataFactory._createCovidClassInstance_() PAST_30_DAYS_CASES report selected")

                if kwargs['MODEL_TYPE'] == CovidModel.PAST_30_DAYS_DECEASED:
                    print ("CovidDataFactory._createCovidClassInstance_() PAST_30_DAYS_DECEASED report selected")

            return "done"
        except:
            print ("CovidMessages.__getData() - unexpected error: ",sys.exc_info()[0])
            return None    

class CovidTotalsToDate(CovidModel):
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
        print("CovidTotalsToDate getData()  kwargs=", kwargs)
        return self.__getData(self, *args, **kwargs)

    def __getData(self, *args, **kwargs):
        try:
            print("CovidTotalsToDate __getData()  kwargs=", kwargs)
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
                print ("CovidTotalsToDate.__getData() - LOCATION param not provided, received: ", kwargs)
                return None       
            return None
        except:
            print ("CovidTotalsToDate.__getData() - unexpected error: ",sys.exc_info()[0])
            return None        
        

 
