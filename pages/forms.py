"""! @brief COVID Traveler Forms package"""
##
# @file forms.py
#
# @brief forms.py defines input form classes ZipCodeForm and for the application.
#
# @section description_forms Description
# This file contains the code that manages the user input forms that enable users to perform searches or contact the application administrator.
#
# @section description_forms Description
# Used to generate forms for user input and persist data using the ORM layer in the models.py package.
# - ZipCodeForm - users enter a zip code to start a search for COVID data for the county and state where the zip code is located.
# - ContactUsForm - users can populate with information requests or other communication that is sent to the system administrator.
#
## @section libraries_forms Libraries/Modules
# - Django imports:
# 	- forms from django
# - Application imports:
# 	- Feedback from pages.models
#
# @section author_forms Author(s)
# - Created by Team #3 on 11/28/2020.
# - Modified by Team #3 on 11/28/2020.
#
# Copyright (c) 2020 COVID Traveler Warning Team.  All rights reserved.

from django import forms
from pages.models import Feedback
#from pages.models import CovidMessages, CovidModelFactory, CovidModel, CovidLocationInfo
#from pages.persistence import DjangoDB, PersistanceRequest

class ZipCodeForm(forms.Form):
	"""! ZipCodeForm creates the zip code input form for COVID-19 user searches. If successful it will return the search_results.html page with text and graphics related to the zip code. 
	"""
	zipCode = forms.CharField(label='Zip code',required=True)
	# stateChoice = forms.ChoiceField(label='State choice ',)
	# countyChoice = forms.ChoiceField(label='County choice ')

	def __init__(self, req, *args, **kwargs):
		"""! The constructor for the class. It accepts several parameters that can be used to control form initialization and related actions. In the v1.0 release there are no actions 
		that require the parameter list, but several functions under development for the v1.1 that require the parameters.

		@param req This contains a Request class object that contains the original http request and information derived from the http request. See the request package for additional
		details.

		@param *args This parameter accepts a python list of parameters passed by a caller. In the v1.0 release there are no actions 
		that require this parameter, but several functions under development for the v1.1 may require this arugument.

		@param **kwargs This parameter accepts a python dictionary of parameters passed by a caller. In the v1.0 release there are no actions 
		that require this parameter, but several functions under development for the v1.1  may require this arugument.
		"""
		super().__init__(*args)
		# if req.state != None:
		# 	self.fields['stateChoice'].choices=self.getStateChoices(req)
		# 	if len(req.state)==0:
		# 		req.state = self.fields['stateChoice'].choices[0][1]
		# 	self.fields['countyChoice'].choices=self.getCountyChoices(req)
		# else:
		# 	req.state = self.fields['stateChoice'].choices[0][1]
		# 	self.fields['countyChoice'].choices=self.getCountyChoices(req)

class ContactUsForm(forms.ModelForm):
	"""! ContactUsForm for the class. It accepts several parameters that can be used to control form initialization and related actions. In the v1.0 release there are no actions 
	that require the parameter list, but several functions under development for the v1.1 that require the parameters.

	@param req This contains a Request class object that contains the original http request and information derived from the http request. See the request package for additional
	details.

	@param *args This parameter accepts a python list of parameters passed by a caller. In the v1.0 release there are no actions 
	that require this parameter, but several functions under development for the v1.1 may require this arugument.

	@param **kwargs This parameter accepts a python dictionary of parameters passed by a caller. In the v1.0 release there are no actions 
	that require this parameter, but several functions under development for the v1.1  may require this arugument.
	"""

	class Meta:
		model = Feedback
		fields = ('name', 'email', 'body')

	# def getStateChoices(self,req):
	# 	"""
	# 	Obtains a list of unique state abbreviations and populates the stateChoice form
	# 	"""
	# 	sql = """
	# 	SELECT distinct state_fullname 
	# 	FROM covidtraveler_db.state_name_xref
	# 	order by state_fullname;
	# 	"""
	# 	dictStates = retrieveDBdata2(req,sql,None)
	# 	return self.convertDictionaryToListOfTuples(dictStates)

	# def getCountyChoices(self,req):
	# 	sql = """
	# 	SELECT county_basename as county
	# 	FROM covidtraveler_db.fips_county_state_names
	# 	WHERE state_fullname = %s;
	# 	"""
	# 	dictCounties = retrieveDBdata2(req,sql,req.STATE_ONLY)
	# 	return self.convertDictionaryToListOfTuples(dictCounties)

	# def getCountyChoicesAsDict(self,req):
	# 	sql = """
	# 	SELECT county_basename as county
	# 	FROM covidtraveler_db.fips_county_state_names
	# 	WHERE state_fullname = %s;
	# 	"""
	# 	choices = retrieveDBdata2(req,sql,req.STATE_ONLY)
	# 	choices = self.setDictKeysEqualToValues(choices)
	# 	return choices

	# def setDictKeysEqualToValues(self,dictList):
	# 	"""
	# 	This takes a list of dictionaries and resets the key to the value itself. For
	# 	example: [{'state' : 'Alabama'}, {'state' : 'Alaska'}] becomes [{'Alabama' : 'Alabama'}, {'Alaska' : 'Alaska'}].
	# 	This is needed for the form select controls.
	# 	"""	
	# 	newDictList=[]
	# 	for item in dictList:
	# 		key, val = next(iter(item.items()))
	# 		temp={}
	# 		temp[val]=val
	# 		newDictList.append(temp)	
	# 	return newDictList	

	# def convertDictionaryToListOfTuples(self, dictionaryList):
	# 	"""
	# 	Converts dictionaryList to a list of tuples
	# 	"""
	# 	tempList=list()
	# 	for i in range(len(dictionaryList)):
	# 		tempList.append(tuple(dictionaryList[i].items())[0])
	# 	return tempList


# def retrieveDBdata2(req,sql,reqType):
# 	"""
# 	... 
# 	"""
# 	from django.db import connection

# 	if reqType == req.ZIPCODE:
# 		data = req.zip
# 	elif reqType in (req.STATE_COUNTY, req.STATE_ONLY):
# 		data = req.state
# 	elif reqType == req.COUNTY_ONLY:
# 		data = req._county_
# 	else:	# just execute the SQL, no params
# 		with connection.cursor() as cursor:
# 			cursor.execute(sql)
# 		return dictFetchRows(cursor)
# 	with connection.cursor() as cursor:
# 		cursor.execute(sql, [data])

# 	return  dictFetchRows(cursor)

# def dictFetchRows(cursor):
# 	"""
# 	Return all rows from cursor as a list of dictionaries
# 	"""
# 	columns = [col[0] for col in cursor.description]
# 	result_list=list()
# 	for row in cursor:
# 		res=dict()
# 		for i in range(len(columns)):
# 			key=columns[i]
# 			res[key] = row[i] 
# 		result_list.append(res)
# 	return result_list
