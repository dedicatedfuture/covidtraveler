from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from pages.request import Request
from pages.forms import ZipCodeForm, ContactUsForm
from pages.persistence import DjangoDB, PersistanceRequest
from pages.models import CovidMessages, CovidModelFactory, CovidModel
import feedparser
from pages.graphics import GraphicsFactory, Graphic
from pages.builder import SearchResultsBuilder, Director
import sys

# Create your views here.

def index(request):
	try:
		if request.method == 'POST': # user entered a zip code and requested a search
			requestObj = Request(request)
			searchBuilder = SearchResultsBuilder()
			director = Director()
			director.setBuilder(searchBuilder)
			context = director.getSearchResults(REQUEST=requestObj)
			if requestObj.errConditionDetected():
				err_msg = requestObj.errMsg
				context = {'err_msg': err_msg}
				return render(request, 'pages/errorpage.html', context)
			else:
				return render(request, 'pages/search_results.html', context)

		else: # home page was just invoked, so render the form that gets user input
			req = Request(request)
			form = ZipCodeForm(req) 
			context={'form': form}
			return render(request, 'base.html', context)
	except:
		print ("views.py index() - unexpected error: ",sys.exc_info()[0])
		return render(request, 'pages/errorpage.html')

def get_county(request):
	from django.http import JsonResponse
	if request.method =='POST' and request.is_ajax():
		req = Request(request, Request.AJAX_REQUEST)
		form = ZipCodeForm(req)
		retval = form.getCountyChoicesAsDict(req)
		retval=[('county', 'Kent'), ('county', 'New Castle'), ('county', 'Sussex')]
		return JsonResponse(retval, safe=False)		

def errorpage(request):
	return render(request, 'pages/errorpage.html')

def contactus(request):

	if request.method == 'POST':
		form = ContactUsForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			form.save()
	form = ContactUsForm()
	return render(request, 'pages/contactus.html', {'form':form})

def news(request):
	url = 'https://tools.cdc.gov/api/v2/resources/media/403372.rss'
	return render(request, 'pages/newsarticles.html', {
		'feed':feedparser.parse(url)
		})

def about(request):
	return render(request, 'pages/about.html')

