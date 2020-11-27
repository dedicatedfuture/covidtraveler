from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from pages.request import Request
from pages.forms import ZipCodeForm, ContactUsForm
from pages.persistence import DjangoDB, PersistanceRequest
from pages.models import CovidMessages, CovidModelFactory, CovidModel
import feedparser
from pages.graphics import GraphicsFactory, Graphic
from pages.builder import SearchResultsBuilder, Director

	# Create your views here.
def index(request):

	# # start testing builder
	# requestObj = Request(request)
	# searchBuilder = SearchResultsBuilder(REQUEST=requestObj)
	# director = Director()
	# director.setBuilder(searchBuilder)
	# director.getSearchResults(REQUEST=requestObj)

	# req = Request(request)
	# form = ZipCodeForm(req) 
	# context={'form': form}

	#return render(request, 'base.html', context)

	if request.method == 'POST':

	# start testing builder
		requestObj = Request(request)
		searchBuilder = SearchResultsBuilder(REQUEST=requestObj)
		director = Director()
		director.setBuilder(searchBuilder)
		result = director.getSearchResults(REQUEST=requestObj)
		print("index() result=", result)
		

		req = Request(request)
		form = ZipCodeForm(req) 
		context={'form': form}
		return render(request, 'base.html', context)

		img2=img1="data:image/png;base64,"
		req = Request(request)
		"""
		AGGREGATE_CASES_DECEASED = 1
		MONTHLY_CASES_DECEASED = 2
		PAST_30_DAYS = 3
		LOCATION_ZIPCODE = 4
		LOCATION_COUNTY = 5
		LOCATION_STATE = 6
		ZIPCODE = 7
		COUNTY = 8
		STATE = 9
		ZIPCODE_COUNTIES = 10
		MODEL_TYPE = 11
		"""
		# img1
		tmpImg=generatePieGraphic(req)
		if tmpImg!=None:
			img1+=tmpImg
		else:	#populate error page
			err_msg = 'No data found for zipcode ' + req.zip 
			context = {'err_msg': err_msg}
			return render(request, 'pages/errorpage.html', context)	
		#return render(request, "pages/search_results.html", context)			

		#img2
		tmpImg=generateStackPlot(req)
		if tmpImg!=None:
			img2+=tmpImg
		else:	#populate error page
			err_msg = 'No data found for zipcode ' + req.zip 
			context = {'err_msg': err_msg}
			return render(request, 'pages/errorpage.html', context)	

		#img3, img4
		img3, img4 = generateDualPlotCases(req)
		if img3==None and img4==None:
			err_msg = 'No data found for zipcode ' + req.zip 
			context = {'err_msg': err_msg}
			return render(request, 'pages/errorpage.html', context)	

		# msgs for zip
		msg_text=''
		data = CovidModelFactory(MODEL_TYPE = CovidModel.MESSAGES, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE=req.zip, ReturnType=DjangoDB.DICTIONARIES )
		if data.DataAvailable:
			print ("CovidModelFactory(MODEL_TYPE=CovidModelFactory.PAST_30_DAYS,ZIPCODE=req.zip,LOCATION=CovidModel.LOCATION_STATE) type(data)=", 
				type(data), "dataAvailable=",data.DataAvailable," data.CovidData=", data.CovidData)
			msg_text = data.CovidData
		else:
			msg_text = None	 			

		# multiple counties for zip
		data = CovidModelFactory(MODEL_TYPE = CovidModel.MESSAGES, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE_COUNTIES=req.zip, ReturnType=DjangoDB.DICTIONARIES )
		if data.DataAvailable:
			if len(data.CovidData) >1:
				print ("CovidModelFactory(MODEL_TYPE=CovidModelFactory.PAST_30_DAYS,ZIPCODE_COUNTIES=req.zip,LOCATION=CovidModel.LOCATION_STATE) type(data)=", 
					type(data), "dataAvailable=",data.DataAvailable," data.CovidData=", data.CovidData)
				msg_text[0]+= " - " + str(data.CovidData).strip('[]')
				
		if msg_text != None:
			context = {'graph1': img1, 'graph2': img2, 'graph3' : img3, 'graph4' : img4, 'msg_text': msg_text[0]}
		else:
			context = {'graph1': img1, 'graph2': img2, 'graph3' : img3, 'graph4' : img4}

		return render(request, "pages/search_results.html", context)		

	else: # home page was just invoked, so render the form that gets user input
		req = Request(request)
		form = ZipCodeForm(req) 
		context={'form': form}
		return render(request, 'base.html', context)

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

def search_results(request):
	return render(request, "pages/search_results.html")


def generatePieGraphic(request):
	data = CovidModelFactory(MODEL_TYPE=CovidModel.AGGREGATE_CASES_DECEASED, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE=request.zip,ReturnType=DjangoDB.DICTIONARIES )
	if data.DataAvailable:
		request_data = data.CovidData
	else:
		return None
		
	pieGraph = GraphicsFactory(GRAPHIC_TYPE=Graphic.PIE, IMAGE_DATA=request_data)
	#print ("generatePieGraphic() pieGraph.image=",pieGraph.image)
	return pieGraph.image


def generateStackPlot(request):

	resultSet = CovidModelFactory(MODEL_TYPE=CovidModel.MONTHLY_CASES_DECEASED, LOCATION=CovidModel.LOCATION_ZIPCODE, ZIPCODE=request.zip,ReturnType=DjangoDB.DICTIONARIES )
	if resultSet.DataAvailable:
		request_data = resultSet.CovidData
	else:
		return None
		
	stackPlotGraph = GraphicsFactory(GRAPHIC_TYPE=Graphic.STACKPLOT, IMAGE_DATA=request_data)
	if stackPlotGraph.ImageAvailable:
		#print ("generateStackPlot() pieGraph.image=",stackPlotGraph.image)
		return stackPlotGraph.image
	else:
		return None


def generateDualPlotCases(req):

	resultSet = CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, 
				LOCATION=CovidModel.LOCATION_ZIPCODE, 
				ZIPCODE=req.zip, ReturnType=DjangoDB.DICTIONARIES )
	if resultSet.DataAvailable:
		county_data = resultSet.CovidData
		#print("generateDualPlotCases county_data=",county_data,"\n")
	else:
		return None	

	# first, get the state for the zipcode
	resultSet = CovidModelFactory(MODEL_TYPE=CovidModel.MESSAGES, 
				ZIPCODE_STATE=req.zip, 
				ReturnType=DjangoDB.DICTIONARIES )
	if resultSet.DataAvailable:
		zip_state = resultSet.CovidData
		#print("generateDualPlotCases state_data=",zip_state_data,"zip_state_data[0]=",zip_state_data[0])
	else:
		return None	

	#next, get the state level data for the zip code exists
	resultSet = CovidModelFactory(MODEL_TYPE=CovidModel.PAST_30_DAYS, LOCATION=CovidModel.LOCATION_STATE,
					 STATE=zip_state[0], ReturnType=DjangoDB.DICTIONARIES )
	if resultSet.DataAvailable:
		state_data = resultSet.CovidData
		#print("generateDualPlotCases state_data=",state_data,"\n")
	else:
		return None	

	dualPlotGraphCases = GraphicsFactory(GRAPHIC_TYPE=Graphic.DUAL_PLOT, COUNTY_DATA=county_data, STATE_DATA=state_data, STATE=zip_state[0])
	if dualPlotGraphCases.ImageAvailable:
		return dualPlotGraphCases.image
	else:
		return None
	

