from django import forms
from . models import Feedback

class ZipCodeForm(forms.Form):
	zipCode = forms.CharField(label='Zip code')
	stateChoice = forms.ChoiceField(label='State choice: ')
	countyChoice = forms.ChoiceField(label='County choice: ')

	def __init__(self, req, *args, **kwargs):
		super().__init__(*args)
		self.fields['stateChoice'].choices=self.setStateChoices(req)

	def setStateChoices(self,req):
		"""
		Obtains a list of unique state abbreviations and populates the stateChoice form
		"""
		from . views import retrieveDBdata
		sql = "select distinct state from covidtraveler_db.US_ZIP_FIPS;"
		dictStates = retrieveDBdata(req,sql)
		return self.convertDictionaryToListOfTuples(dictStates)

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

