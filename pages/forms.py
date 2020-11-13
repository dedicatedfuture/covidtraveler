from django import forms
from pages.models import Feedback



class ZipCodeForm(forms.Form):
	zipCode = forms.CharField(label='Zip code')
	stateChoice = forms.ChoiceField(label='State choice: ')
	countyChoice = forms.ChoiceField(label='County choice: ')

	def __init__(self, req, county="", *args, **kwargs):
		super().__init__(*args)
		self.fields['stateChoice'].choices=self.setStateChoices(req)
		self.fields['countyChoice'].choices=self.setCountyChoices(req)

	def setStateChoices(self,req):
		"""
		Obtains a list of unique state abbreviations and populates the stateChoice form
		"""
		from . views import retrieveDBdata
		sql = "select distinct state from covidtraveler_db.US_ZIP_FIPS;"
		dictStates = retrieveDBdata(req,sql)
		return self.convertDictionaryToListOfTuples(dictStates)

	def setCountyChoices(self,req):
		from . views import retrieveDBdata2
		sql = "select distinct countyname from covidtraveler_db.US_ZIP_FIPS where STATE=%s;"
		dictCounties = retrieveDBdata2(req,sql,req.STATE_ONLY)
		print("county query: ", sql)
		print("county dictcounties: ", dictCounties)
		return self.convertDictionaryToListOfTuples(dictCounties)


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
