from django.test import TestCase, Client
from django.urls import reverse
from pages import request
import json



class TestViews(TestCase):

	#called before other test cases to build test files
	def setUp(self):
		self.client = Client()
		self.index = reverse('index')
		self.contactus = reverse('contactus')
		self.news = reverse('news')
		self.about = reverse('about')
		self.search_results = reverse('search_results')
		self.search_type = 3


	#Test proves REST GET response renders base template, 
	#can alter if more templates used
	def test_index_GET(self):
		response = self.client.get(self.index)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'base.html')

	def test_index_POST(self):
		response = self.client.post(self.index)
		self.assertEquals(response.status_code, 302)
		self.assertTemplateUsed(response, 'pages/search_results.html')

	def test_contactus_GET(self):
		response = self.client.get(self.contactus)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'pages/contactus.html')

	def test_contactus_POST(self):
		response = self.client.post(self.contactus)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'pages/contactus.html')
		
	def test_news_GET(self):
		response = self.client.get(self.news)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'pages/newsarticles.html')		

	def test_about_GET(self):
		response = self.client.get(self.about)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'pages/about.html')	

	def test_searchresults_GET(self):
		response=self.client.get(self.search_results)
		self.assertEquals(response.status_code, 200)
		self.assertTemplateUsed(response, 'pages/search_results.html')