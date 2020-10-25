from django.test import TestCase, Client
from django.urls import reverse
import json

class TestModels(TestCase):

	# def test_UsZipFips(self)
	# 	self.assertEquals(1, 1)

	#Test proves REST GET response renders base template, 
	#can alter if more templates used
	# def test_index_GET(self):
		
	# 	response = self.client.get(self.index)
	# 	self.assertEquals(response.status_code, 200)
	# 	self.assertTemplateUsed(response, 'base.html')

	# def test_contactus_GET(self):
		
	# 	response = self.client.get(self.contactus)
	# 	self.assertEquals(response.status_code, 200)
	# 	self.assertTemplateUsed(response, 'base.html')
		
	# def test_news_GET(self):
		
	# 	response = self.client.get(self.news)
	# 	self.assertEquals(response.status_code, 200)
	# 	self.assertTemplateUsed(response, 'base.html')		

	# def test_about_GET(self):
		
	# 	response = self.client.get(self.about)
	# 	self.assertEquals(response.status_code, 200)
	# 	self.assertTemplateUsed(response, 'base.html')
	 