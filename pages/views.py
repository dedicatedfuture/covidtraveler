from django.shortcuts import render
from django.http import HttpResponse
from . models import UsZipFipsV2
import feedparser

# Create your views here.
def index(request):
	#return HttpResponse("<h1>Hello World!</h1>")
	print("index served")
	return render(request, 'base.html')


def contactus(request):
	return render(request, 'pages/contactus.html')

def news(request):
	url = 'https://tools.cdc.gov/api/v2/resources/media/403372.rss'
	feed = feedparser.parse(url)
	return render(request, 'pages/newsarticles.html', {
		'feed':feed
		})

def about(request):
	return render(request, 'pages/about.html')

#def us_states(request, pagename):
def us_states(request):
	context = {
		'state': UsZipFipsV2.state,
		'county': UsZipFipsV2.countyname,
		'state': UsZipFipsV2.state,
		'fips': UsZipFipsV2.stcountyfips,
		'fips_list': UsZipFipsV2.objects.all()[0:15],
	}
	#print(context)
	#assert False
	return render(request, 'pages/us_states.html', context)
