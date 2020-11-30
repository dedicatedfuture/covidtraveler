"""! @brief COVID Traveler URL handlers - invokes application code to respond to http requests"""

##
# @file views.py
#
# @brief The views.py package manages all http requests passed from the Django framework and returns a page in response.
#
# @section description_views Description
# This file contains the handler code that invokes application functionality that responds to user requests Django framework.
# There are currently four handlers that are actively servicing requests:
# - index - for the home page 
# - contactus - a simple page for users that need to contact the admin with a message
# - news - a newsfeed of CDC information that is current with relevant news articles
# - about - a static page with information about the website
#  
# @section libraries_views Libraries/Modules
# - imports:
# 	- render from django.shortcuts
# 	- HttpResponse, HttpRequest from django.http
# 	- feedparser (python package)
# - Application packages
# 	- SearchResultsBuilder, Director from pages.builder
#	- ZipCodeForm, ContactUsForm from pages.forms
#	- Request from pages.request
#
# @section author_views Author(s)
# - Created by Team #3 on 11/28/2020.
# - Modified by Team #3 on 11/28/2020.
#
# Copyright (c) 2020 COVID Traveler Warning Team.  All rights reserved.

from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from pages.request import Request
from pages.forms import ZipCodeForm, ContactUsForm
import feedparser, sys
from pages.builder import SearchResultsBuilder, Director

from django.core.handlers.wsgi import WSGIRequest
from io import StringIO
from django.http.request import QueryDict


# Create your views here.

def index(request):
	"""! Receives http GET/POST requests from callers. If a GET is received, then simply return the home page which contains the zip code search fields. 
	If a POST is received, invoke the Request, SearchResultsBuilder and Director class methods to generate a response. 
	
	@param request	The http request object passed to this function by the Django framework. It contains information needed to service the request such 
	as search form input fields (zip code) and whether the call is an AJAX call for data refresh of a page element

	@return If no error is encountered, the fully rendered search_results.html page, otherwise the error_page.html with information regarding the error

	"""
	# qd = QueryDict('POST=19061')

	# fakeWSGIRequest = WSGIRequest({

	# 	'REQUEST_METHOD': 'POST={zipCode=19061',
	# 	'PATH_INFO': '/',
	# 	'wsgi.input': StringIO(),
	# 	})

	# #fakeWSGIRequest.PO
	# #print('fake wsgri type: ', type(fakeWSGIRequest.POST), "fakeWSGIRequest type=",type(fakeWSGIRequest))
	# #print('request type=',type(request), "request.POST type=",type(request.POST))
	# print('fakeWSGIRequest.POST=',fakeWSGIRequest.POST)
	# print('fakeWSGIRequest.POST.get()',fakeWSGIRequest.POST.get())
	
	
	try:
		if request.method == 'POST': # user entered a zip code and requested a search
			requestObj = Request(request)
			searchBuilder = SearchResultsBuilder()
			director = Director()
			director.setBuilder(searchBuilder)
			if director.getSearchResults(REQUEST=requestObj):
				return render(request, 'pages/search_results.html', requestObj.getContext())
			else:
				err_msg = requestObj.errMsg
				context = {'err_msg': err_msg}
				return render(request, 'pages/errorpage.html', context)				

		else: # home page was just invoked, so render the form that gets user input
			req = Request(request)
			form = ZipCodeForm(req) 
			context={'form': form}
			return render(request, 'base.html', context)
	except:
		print ("views.py index() - unexpected error: ",sys.exc_info()[0])
		return render(request, 'pages/errorpage.html')

# def get_county(request): # used for an AJAX request - currently under development for v1.1
# 	from django.http import JsonResponse
# 	if request.method =='POST' and request.is_ajax():
# 		req = Request(request, Request.AJAX_REQUEST)
# 		form = ZipCodeForm(req)
# 		retval = form.getCountyChoicesAsDict(req)
# 		return JsonResponse(retval, safe=False)		

# def errorpage(request):	# currently under development for v1.1
# 	return render(request, 'pages/errorpage.html')

def contactus(request):
	"""! Receives http contactus GET/POST requests from callers to retrieve the Contact form.

	@param request	The http request object passed to this function by the Django framework. If a POST request is received it will contain the 'name', 'email', and 'body'
	fields with data from the user to save to the database.

	@return If no error is encountered, a blank contact form page in response to a GET. If the http request was POST, then the content is saved and a blank contact 
	form will be returned to the sender.
	"""
	if request.method == 'POST':
		form = ContactUsForm(request.POST)
		if form.is_valid():
			form.save()
	form = ContactUsForm()
	return render(request, 'pages/contactus.html', {'form':form})

def news(request):
	"""! Receives http GET/POST requests from callers to retrieve a news feed. This method doesn't distinguish between GET/POST because no parameters are received. 

	@param request	The http request object passed to this function by the Django framework. The request will have no parameters.

	@return If no error is encountered, a news feed from the CDC will be returned with links to current articles related ot COVID-19.  
	"""
	url = 'https://tools.cdc.gov/api/v2/resources/media/403372.rss'
	return render(request, 'pages/newsarticles.html', {
		'feed':feedparser.parse(url)
		})

def about(request):
	return render(request, 'pages/about.html')

