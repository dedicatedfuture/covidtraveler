"""
This package contains all persistance related classes and methods
"""
from django.db import connection
from abc import ABC, abstractmethod
import sys

class Persistance(ABC):
    """
    This is the abstract class for all persistence activity performed against a datastore.
    """

    # constants
    SQLDB=1
    FLAT_FILE=2
    SQL_QUERY=3
    DICTIONARIES=4
    TUPLES=5

    def __init__(self):
        super().__init__()
        
    def getData(self, dataRequest):
        """
        This is the abstract method for retrieving data from a data store.
        """
        raise NotImplementedError

class PersistanceRequest:
    """
    The PersistanceRequest class is a concrete class used to prepare persistance instructions
    and parameters for use with a data store.
    """
    def __init__(self, *args, **kwargs ):
        self._parseArgs_(*args, **kwargs)
        
    def _parseArgs_(self, *args, **kwargs):
        self.argList=args
        self.argDict=kwargs        

class DjangoDB(Persistance):

    def __init__(self):
        super().__init__()

    def getData(self, persistanceRequest):
        """
        This is a concrete method for retrieving data from a database using Django's database access. The persistanceRequest is
        an instance of the persistanceRequest class that contains the information needed for this
        data retrieval activity such as a SQL statement and variable list of parameters
        """
        try:
            if 'SQL' in persistanceRequest.argDict:
                # expect to find a dictionary item named 'SQL'
                self.sql=persistanceRequest.argDict['SQL']
                # print ("getData() SQL=",self.sql)

            # look for params
            if 'whereParams' in persistanceRequest.argDict:
                # expect to find a dictionary item named 'SQL'
                self.data=persistanceRequest.argDict['whereParams']

            # look to see if the return collection type is specified; default to dictionaries
            if 'ReturnType' in persistanceRequest.argDict and persistanceRequest.argDict['ReturnType']==self.TUPLES:
                return self._fetchRowsAsTuples_(self._retrieveDBdata_(self.sql, self.data))
            
            else: #default to dictionaries
                return self._fetchRowsAsDict_(self._retrieveDBdata_(self.sql, self.data))
            
        except:
            print ("DjangoDB.getData() - unexpected error: ",sys.exc_info()[0])
            return None

            
    def _retrieveDBdata_(self, sql, data):
        """
        ... 
        """
        from django.db import connection
        try:
            with connection.cursor() as cursor:
                cursor.execute(sql, data)
            return cursor
        except:
            print ("DjangoDB._retrieveDBdata_() - unexpected error: ",sys.exc_info()[0])
            return None

    def _fetchRowsAsDict_(self, cursor):
        """
        Return all rows from cursor as a list of dictionaries
        """
        try:
            columns = tuple(col[0] for col in cursor.description)
            result_list=list()
            for row in cursor:
                res=dict()
                for i in range(len(columns)):
                    key=columns[i]
                    res[key] = row[i] 
                result_list.append(res)
            return result_list
        except:
            print ("DjangoDB._fetchRowsAsDict_() - unexpected error: ",sys.exc_info()[0])
            return None            

    def _fetchRowsAsTuples_(self, cursor):
        """
        Return all rows from cursor as two lists: columns, rows
        """
        try:
            columns = tuple(col[0] for col in cursor.description)
            for row in cursor:
                rows=list()
                rows.append(row)
            return columns, rows
        except:
            print ("DjangoDB._fetchRowsAsTuples_() - unexpected error: ",sys.exc_info()[0])
            return None            


