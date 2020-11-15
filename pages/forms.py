from django import forms
from pages.models import Feedback

class ZipCodeForm(forms.Form):
	zipCode = forms.CharField(label='Zip code')
	stateChoice = forms.ChoiceField(label='State choice ')
	countyChoice = forms.ChoiceField(label='County choice ')

	def __init__(self, req, *args, **kwargs):
		super().__init__(*args)
		if req.state != None:
			if  req.state != self.fields['stateChoice'].choices[0][1]:
				self.fields['stateChoice'].choices=self.getStateChoices(req)
				print("ZipCodeForm() __init__, req.state=",req.state," self.fields['stateChoice'].choices=",self.fields['stateChoice'].choices)
				self.fields['countyChoice'].choices=self.getCountyChoices(req)		
		else:
			req.state = self.fields['stateChoice'].choices[0][1]
			print("ZipCodeForm() __init__, req.state=",req.state)
			self.fields['countyChoice'].choices=self.getCountyChoices(req)


	def getStateChoices(self,req):
		"""
		Obtains a list of unique state abbreviations and populates the stateChoice form
		"""
		from . views import retrieveDBdata2
		sql = """
		SELECT distinct state_fullname 
		FROM covidtraveler_db.state_name_xref
		order by state_fullname;
		"""
		dictStates = retrieveDBdata2(req,sql,None)
		return self.convertDictionaryToListOfTuples(dictStates)

	def getCountyChoices(self,req):
		from . views import retrieveDBdata2
		sql = """
		SELECT county_basename as county
		FROM covidtraveler_db.fips_county_state_names
		WHERE state_fullname = %s;
		"""
		print("setCountyChoices req.state=",req.state," county query: ", sql)
		dictCounties = retrieveDBdata2(req,sql,req.STATE_ONLY)
		#print("county dictcounties: ", dictCounties)
		return self.convertDictionaryToListOfTuples(dictCounties)

	def setCountyChoices(self,req):
		#self.fields['countyChoice'].choices=self.getCountyChoices(req)
		self.fields['countyChoice'].choices=[('county', 'Kent'), ('county', 'New Castle'), ('county', 'Sussex')]
		print("setCountyChoices() self.fields['countyChoice'].choices=",self.fields['countyChoice'].choices)


	def convertDictionaryToListOfTuples(self, dictionaryList):
		"""
		Converts dictionaryList to a list of tuples
		"""
		tempList=list()
		for i in range(len(dictionaryList)):
			tempList.append(tuple(dictionaryList[i].items())[0])
		#print ("convertDictionaryToListOfTuples() templist=",tempList)
		return tempList

class ContactUsForm(forms.ModelForm):

	class Meta:
		model = Feedback
		fields = ('name', 'email', 'body')
