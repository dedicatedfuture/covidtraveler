from django.test import SimpleTestCase
from django.urls import reverse, resolve
from pages.views import index, contactus, news, about

#These unit tests check that the views match the urls
class TestUrls(SimpleTestCase):

	def test_index_url_is_resolved(self):
		url = reverse('index')
		print('test_index_url_is_resolved running...')
		self.assertEquals(resolve(url).func, index)
		print(resolve(url))


	def test_contactus_url_is_resolved(self):
		url = reverse('contactus')
		print('test_contactus_url_is_resolved running...')
		self.assertEquals(resolve(url).func, contactus)
		print(resolve(url))

	def test_news_url_is_resolved(self):
		url = reverse('news')
		print('test_news_url_is_resolved running...')
		self.assertEquals(resolve(url).func, news)
		print(resolve(url))

	def test_about_url_is_resolved(self):
		url = reverse('about')
		print('test_about_url_is_resolved running...')
		self.assertEquals(resolve(url).func, about)
		print(resolve(url))
