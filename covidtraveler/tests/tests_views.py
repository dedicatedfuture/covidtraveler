from django.test import TestCase, Client
from django.urls import reverse
import json



class TestViews(TestCase):

	#called before other test cases to build test files
	def setUp(self):
		self.client = Client()
		self.index = reverse('index')
		self.contactus = reverse('contactus')
		self.news = reverse('news')
		self.about = reverse('about')
		self.us_states = reverse('us_states')


	#Test proves REST GET response renders base template, 
	#can alter if more templates used
	def test_index_GET(self):
		
		response = self.client.get(self.index)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'base.html')

	def test_index_POST(self):

		response = self.client.post(self.index)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'base.html')

	def test_contactus_GET(self):
		
		response = self.client.get(self.contactus)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'base.html')

	def test_contactus_POST(self):

		response = self.client.post(self.contactus)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'base.html')
		
	def test_news_GET(self):
		
		response = self.client.get(self.news)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'base.html')		

	def test_about_GET(self):
		
		response = self.client.get(self.about)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'base.html')	

	#def test_states_GET(self):
	#	response = self.client.get(self.us_states)
	#	self.assertEquals(response.status_code, 200)
	#ß	self.assertTemplateUsed(response, 'base.html')	