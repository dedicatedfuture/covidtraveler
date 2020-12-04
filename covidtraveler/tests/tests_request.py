from django.test import TestCase, Client
from django.urls import reverse
from pages.request import Request
from django.core.handlers.wsgi import WSGIRequest
from io import StringIO
import json

class TestRequest(TestCase):

	def test_request_zip(self):
		self.client = Client()
		self.index = reverse('index')

		fakeWSGIRequest = WSGIRequest({
          'REQUEST_METHOD': 'POST',
          'PATH_INFO': '/',
          'wsgi.input': StringIO()
          })

		req = Request(fakeWSGIRequest)
		req.search_type = 4
		self.assertEquals(req.search_type, 4)
