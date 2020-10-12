from django import forms

class ZipCodeForm(forms.Form):
	#zipCode = forms.RegexField(label='Zip code')
	zipCode = forms.CharField(label='Zip code')
