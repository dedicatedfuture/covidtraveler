from django.test import SimpleTestCase
from pages.forms import ZipCodeForm

class TestForms(SimpleTestCase):

	def test_zip_code_valid_data(self):
		form = ZipCodeForm(data={
			'zipCode': 19061
			})

		self.assertTrue(form.is_valid())


	def test_zip_code_form_no_data(self):
		form = ZipCodeForm(data={})

		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors), 1)