from django.test import SimpleTestCase
from django.urls import reverse, resolve
from pages.views import index, contactus, news, about, search_results, errorpage

#These unit tests check that the views match the urls
class TestUrls(SimpleTestCase):

	def test_index_url_is_resolved(self):
		url = reverse('index')
		self.assertEquals(resolve(url).func, index)
		print(resolve(url))

	def test_errorpage_url_is_resolved(self):
		url = reverse('errorpage')
		self.assertEquals(resolve(url).func, errorpage)
		print(resolve(url))

	def test_contactus_url_is_resolved(self):
		url = reverse('contactus')
		self.assertEquals(resolve(url).func, contactus)
		print(resolve(url))

	def test_news_url_is_resolved(self):
		url = reverse('news')
		self.assertEquals(resolve(url).func, news)
		print(resolve(url))

	def test_about_url_is_resolved(self):
		url = reverse('about')
		self.assertEquals(resolve(url).func, about)
		print(resolve(url))

	def test_search_results_is_resolved(self):
		url = reverse('search_results')
		print("search result test: ")
		print(resolve(url))
		self.assertEquals(resolve(url).func, search_results)

