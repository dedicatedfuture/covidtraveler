from django.shortcuts import render
from django.http import HttpResponse
from . models import UsZipFipsV2
from .forms import ZipCodeForm
import feedparser

# Create your views here.
def index(request):
	#return HttpResponse("<h1>Hello World!</h1>")
	print("index served")
	form = ZipCodeForm()
	
	context={'form': form}
	if request.method == 'POST':
		print(request.POST)
		zip_code=ZipCodeForm(request.POST)
		context = {'zip_code': zip_code}
		#TO_DO send zip_code to model
	return render(request, 'base.html', context)


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
