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


	#Test proves REST GET response renders base template, 
	#can alter if more templates used
	def test_index_GET(self):
		
		response = self.client.get(self.index)
		print('test_index_GETrunning...')
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'base.html')

	def test_contactus_GET(self):
		
		response = self.client.get(self.contactus)
		print('test_contactus_GET running...')
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'base.html')
		
	def test_news_GET(self):
		
		response = self.client.get(self.news)
		print('test_news_GET running...')
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'base.html')		

	def test_about_GET(self):
		
		response = self.client.get(self.about)
		print('test_about_GET running...')
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'base.html')	