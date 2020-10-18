from django import forms
from pages.models import Feedback

class ZipCodeForm(forms.Form):
	#zipCode = forms.RegexField(label='Zip code')
	zipCode = forms.CharField(label='Zip code')


class ContactUsForm(forms.ModelForm):

	class Meta:
		model = Feedback
		fields = ('name', 'email', 'body')
