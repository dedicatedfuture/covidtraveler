from django.test import SimpleTestCase, TestCase, Client
from django.urls import reverse, resolve
from pages.forms import ZipCodeForm
from pages.forms import ContactUsForm
from pages.request import Request

class TestForms(SimpleTestCase):

	def setUp(self):
		self.client = Client()
		self.index = reverse('index')
		response = self.client.post(self.index)
		req = Request(response)
		Request.objects.create(req, zipCode='19061', state='PA', county='Delaware')

	def test_zip_code_valid_data(self):
		form = ZipCodeForm(data={
			'zipCode': 19061,
			'stateChoice': 'DE',
			'countyChoice': 'Kent'
			})
		self.assertTrue(form.is_valid())

	def test_getCountyChoices(self):
		response = self.client.post(self.index)
		req = Request(response)
		form = ZipCodeForm(req, data={
			'zipCode': 19061,
			'stateChoice': 'DE',
			'countyChoice': 'Kent'
			})
		form.getCountyChoices()

		self.assertEqual(form.getCountyChoices(), (('Alabama', 'Kent'), ('Delaware', 'New Castle'), ('county', 'Sussex')))




	def test_zip_code_form_no_data(self):
		
		response = client.post(index)

		req = Request(response)
		form = ZipCodeForm(req, data={})

		self.assertFalse(form.is_valid())
		self.assertEquals(len(form.errors), 2)

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




