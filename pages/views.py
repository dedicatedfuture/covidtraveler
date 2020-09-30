from django.shortcuts import render
from django.http import HttpResponse
import feedparser

# Create your views here.
def index(request):
	#return HttpResponse("<h1>Hello World!</h1>")
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
