from django.test import TestCase, Client
from django.urls import reverse
from pages import request
import json

class TestRequest(TestCase):

	def test_request_zip(self):
		self.index = reverse('index')
		response = self.client.post(self.index, {
			'search_type': '3'
			})

		req = Request(response).search_type = 3

		self.assertEquals(req.search_type, 3)
