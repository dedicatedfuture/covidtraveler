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
    
    _persist_ = DjangoDB()

    def __init__(self, *args, **kwargs):
        super().__init__()

    def _getData_(self, *args, **kwargs):
        raise NotImplementedError

    def dataAvailableForRequest(self, *args, **kwargs):
        raise NotImplementedError

class CovidMessages(CovidModel):
    _argList_ = []
    _argDict_ = {} 
    _sql_ = ''
    _data_ = None 

    def __init__(self, *args, **kwargs):
        super().__init__()
        #self._persist_ = DjangoDB()
        _argList_=args
        _argDict_=kwargs   
              
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

    def _getData_(self, *args, **kwargs):
        try:
            self.dbReq = PersistanceRequest(ReturnType=DjangoDB.DICTIONARIES, SQL=kwargs['SQL'], whereParams=[kwargs['whereParams']])
            return self._persist_.getData(self.dbReq)
        except:
            print ("CovidMessages._getData_() - unexpected error: ",sys.exc_info()[0])
            return None        
        
    def dataAvailableForRequest(self, *args, **kwargs):
        pass

    def getMessages(self, *args, **kwargs):
        try:
            if 'ZIPCODE' in kwargs:                
                self._sql_=self._sqlZipMsgs_
                self._data_=[kwargs['ZIPCODE']]
    
            elif 'STATE' in kwargs and 'COUNTY' in kwargs: #only interested in case where both are populated
                self._sql_=self._sqlCountyMsgs_
                self._data_=[kwargs['STATE'],kwargs['COUNTY']]
            
            else:
                print ("CovidMessages.getMessages() - missing expected keys ZIPCODE or STATE/COUNTY combination in argument list - received: ",kwargs)
                return None
            
            self._result_ = self._getData_(SQL=self._sql_, whereParams=self._data_)
            self._msg_ = [d.get('msg_text', None) for d in self._result_]

            if self._msg_ != None:
                return self._msg_
            else:
                return None
        except:
            print ("CovidMessages.getMessages() - unexpected error: ",sys.exc_info()[0])
            return None

class CovidDataFactory:
    """
    This concrete class uses a simple parameterized approach to constructing the required CovidData subclass
    needed by the consumer.
    """
    _argList_=[]
    _argDict_={}
    TO_DATE_TOTALS_CASES_DECEASED = 1
    MONTHLY_TOTALS_CASES_DECEASED = 2
    PAST_30_DAYS_CASES = 3
    PAST_30_DAYS_DECEASED = 4

    def __init__(self, *args, **kwargs):
        _argList_=args
        _argDict_=kwargs
        self._createCovidClassInstance_()

    def _createCovidClassInstance_(self):
        """
        Use the args to identify the ideal class
        """
        try:
            if 'GRAPH_TYPE' in self._argDict_:
                if self._argDict_['GRAPH_TYPE'] == CovidDataFactory.TO_DATE_TOTALS_CASES_DECEASED:
                    print ("CovidDataFactory._createCovidClassInstance_() TO_DATE_TOTALS_CASES_DECEASED report selected")

                if self._argDict_['GRAPH_TYPE'] == CovidDataFactory.MONTHLY_TOTALS_CASES_DECEASED:
                    print ("CovidDataFactory._createCovidClassInstance_() MONTHLY_TOTALS_CASES_DECEASED report selected")

                if self._argDict_['GRAPH_TYPE'] == CovidDataFactory.PAST_30_DAYS_CASES:
                    print ("CovidDataFactory._createCovidClassInstance_() PAST_30_DAYS_CASES report selected")

                if self._argDict_['GRAPH_TYPE'] == CovidDataFactory.PAST_30_DAYS_DECEASED:
                    print ("CovidDataFactory._createCovidClassInstance_() PAST_30_DAYS_DECEASED report selected")

            return "done"
        except:
            print ("CovidMessages._getData_() - unexpected error: ",sys.exc_info()[0])
            return None        
        
