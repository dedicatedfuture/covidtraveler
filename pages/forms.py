from django import forms
from pages.models import Feedback

class StateField(forms.MultiValueField):

	def __init__(self, *args, **kwargs):

		fields = (
			forms.CharField(),
			forms.CharField()
		)

		super().__init__(fields, *args, **kwargs)
	def compress(self, data_list):
		data_list = ['PA', 'NJ']
		return f'{data_list[0]} {data_list[1]}'

class ZipCodeForm(forms.Form):
	#zipCode = forms.RegexField(label='Zip code')
	zipCode = forms.CharField(label='Zip code')
	stateChoices = (('PA', 'PA'), ('DE', 'DE'),('CA', 'CA'))
	stateChoice = forms.ChoiceField(choices = stateChoices, label='State choice: ')
		


class ContactUsForm(forms.ModelForm):

	class Meta:
		model = Feedback
		fields = ('name', 'email', 'body')
