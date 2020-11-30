from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from pages.forms import ZipCodeForm
from pages.forms import ContactUsForm
from pages.request import Request

class TestForms(TestCase):

	def setUp(self):
		self.client = Client()
		self.index = reverse('index')
		

	def test_zip_code_valid_data(self):
		req = Request(self.client.post(self.index, {'zipCode': 19061}))
		form = ZipCodeForm(req, data={
			'zipCode': 19061
			})
		self.assertTrue(form.is_valid())

	#def test_getCountyChoices(self):
	#	response = self.client.post(self.index)
	#	req = Request(response)
	#	form = ZipCodeForm(req, data={
	#		'zipCode': 19061,
	#		'stateChoice': 'DE',
	#		'countyChoice': 'Kent'
	#		})
	#	form.getCountyChoices()

	#	self.assertEqual(form.getCountyChoices(), (('Alabama', 'Kent'), ('Delaware', 'New Castle'), ('county', 'Sussex')))




	def test_zip_code_form_no_data(self):
		
		response = self.client.post(self.index)

		req = Request(response)
		form = ZipCodeForm(req, data={})

		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors), 1)

	def test_contactus_valid_data(self):
		form = ContactUsForm(data={
			'name':'John Doe', 
			'email': 'test@test.com', 
			'body': 'This is a test submission'
			})
		self.assertTrue(form.is_valid())

	def test_contactus_form_no_data(self):
		form = ContactUsForm(data={})

		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors), 3)
