from django import forms
from pages.models import Feedback, CovidMessages, CovidModelFactory, CovidModel, CovidLocationInfo
from pages.persistence import DjangoDB, PersistanceRequest

class ZipCodeForm(forms.Form):
	zipCode = forms.CharField(label='Zip code',required=True)
	# stateChoice = forms.ChoiceField(label='State choice ',)
	# countyChoice = forms.ChoiceField(label='County choice ')

	def __init__(self, req, *args, **kwargs):
		super().__init__(*args)
		# if req.state != None:
		# 	self.fields['stateChoice'].choices=self.getStateChoices(req)
		# 	if len(req.state)==0:
		# 		req.state = self.fields['stateChoice'].choices[0][1]
		# 	self.fields['countyChoice'].choices=self.getCountyChoices(req)
		# else:
		# 	req.state = self.fields['stateChoice'].choices[0][1]
		# 	self.fields['countyChoice'].choices=self.getCountyChoices(req)


	def getStateChoices(self,req):
		"""
		Obtains a list of unique state abbreviations and populates the stateChoice form
		"""
		sql = """
		SELECT distinct state_fullname 
		FROM covidtraveler_db.state_name_xref
		order by state_fullname;
		"""
		dictStates = retrieveDBdata2(req,sql,None)
		return self.convertDictionaryToListOfTuples(dictStates)
		#return (('Alabama', 'Kent'), ('Delaware', 'New Castle'), ('county', 'Sussex'))

	def getCountyChoices(self,req):
		sql = """
		SELECT county_basename as county
		FROM covidtraveler_db.fips_county_state_names
		WHERE state_fullname = %s;
		"""
		dictCounties = retrieveDBdata2(req,sql,req.STATE_ONLY)
		return self.convertDictionaryToListOfTuples(dictCounties)

	def getCountyChoicesAsDict(self,req):
		sql = """
		SELECT county_basename as county
		FROM covidtraveler_db.fips_county_state_names
		WHERE state_fullname = %s;
		"""
		choices = retrieveDBdata2(req,sql,req.STATE_ONLY)
		choices = self.setDictKeysEqualToValues(choices)
		return choices

	def setDictKeysEqualToValues(self,dictList):
		"""
		This takes a list of dictionaries and resets the key to the value itself. For
		example: [{'state' : 'Alabama'}, {'state' : 'Alaska'}] becomes [{'Alabama' : 'Alabama'}, {'Alaska' : 'Alaska'}].
		This is needed for the form select controls.
		"""	
		newDictList=[]
		for item in dictList:
			key, val = next(iter(item.items()))
			temp={}
			temp[val]=val
			newDictList.append(temp)	
		return newDictList	

	def convertDictionaryToListOfTuples(self, dictionaryList):
		"""
		Converts dictionaryList to a list of tuples
		"""
		tempList=list()
		for i in range(len(dictionaryList)):
			tempList.append(tuple(dictionaryList[i].items())[0])
		return tempList

class ContactUsForm(forms.ModelForm):

	class Meta:
		model = Feedback
		fields = ('name', 'email', 'body')

def retrieveDBdata2(req,sql,reqType):
	"""
	... 
	"""
	from django.db import connection

	if reqType == req.ZIPCODE:
		data = req.zip
	elif reqType in (req.STATE_COUNTY, req.STATE_ONLY):
		data = req.state
	elif reqType == req.COUNTY_ONLY:
		data = req._county_
	else:	# just execute the SQL, no params
		with connection.cursor() as cursor:
			cursor.execute(sql)
		return dictFetchRows(cursor)
	with connection.cursor() as cursor:
		cursor.execute(sql, [data])

	return  dictFetchRows(cursor)

def dictFetchRows(cursor):
	"""
	Return all rows from cursor as a list of dictionaries
	"""
	columns = [col[0] for col in cursor.description]
	result_list=list()
	for row in cursor:
		res=dict()
		for i in range(len(columns)):
			key=columns[i]
			res[key] = row[i] 
		result_list.append(res)
	return result_list
