from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . models import UsZipFips, CovidFinalmasterTable
from . forms import ZipCodeForm
import feedparser, matplotlib.pyplot as plt, base64
from io import StringIO, BytesIO
from PIL import Image
from matplotlib.patches import Shadow
from django.db import connection

from django.http import HttpResponse
from .models import UsZipFips
from .forms import ZipCodeForm
from .forms import ContactUsForm
import feedparser

# Create your views here.
def index(request):
	# this code renders the form that gets user input
	form = ZipCodeForm()
	context={'form': form}

	# after user enters input, this code will fire because of the POST action by the user clicking Submit
	if request.method == 'POST':
		# context = {
		# 	'zips_list': UsZipFips.objects.filter(zip=request.POST.get("zipCode")).values(),
		# }
		img2=img1="data:image/jpg;base64,"
		img1+=generatePieGraphic(request)
		img2+=generateStackPlot(request)
		context = {'graph1': img1, 'graph2': img2, 'county1': '-- Montgomery --','county2': '-- Delaware --'}
		return render(request, "pages/search_results.html", context)
		#print("context=", context)	

	return render(request, 'base.html', context)

def showStates(request):
	#states=UsZipsFips.zip.objects.all()
	states=["PA", "NJ", "MD", "DE"]
	print("showStates Served")
	return render(request, "ShowStates.html", {"showStates": states})


def contactus(request):

	if request.method == 'POST':
		form = ContactUsForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			email = form.cleaned_data['email']
			print(name, email)
			form.save()
	form = ContactUsForm()
	return render(request, 'pages/contactus.html', {'form':form})

def news(request):
	url = 'https://tools.cdc.gov/api/v2/resources/media/403372.rss'
	feed = feedparser.parse(url)
	for item in feed.entries:
		item.published = item.published[0:16]
		print(item.published[0:16])
		print(type(item))
	
	return render(request, 'pages/newsarticles.html', {
		'feed':feed
		})

def about(request):
	return render(request, 'pages/about.html')

def search_results(request):
	return render(request, "pages/search_results.html")

def generatePieGraphic(request):
	# Pie chart, where the slices will be ordered and plotted counter-clockwise:
	# make a square figure and axes

	sql = """SELECT uzf.zip AS ZIP, uzf.STcountyFIPS AS FIPS, cft.county AS County, cft.province_state AS State,
		SUM(cft.daily_confirmed_case) AS Cases, SUM(cft.daily_deaths_case) AS Deceased 
		FROM covid_finalmaster_table cft JOIN US_ZIP_FIPS uzf ON ((cft.FIPS = uzf.STcountyFIPS)) 
		WHERE uzf.zip = %s 
		GROUP BY uzf.zip , uzf.STcountyFIPS , cft.county , cft.province_state """
	request_data = retrieveDBdata(request,sql) ## has an issue
	#print("B-request_data=",request_data)

	# can only generate graph if data available
	if len(request_data) > 0:
		labels = 'Cases', 'Deceased'
		for i in range(len(request_data)):
			print ("request_data=",request_data[i])
		county = request_data[0]['County']
		print ("county=",county)

		#  case = 100*(Cases-Deceased)/Cases
		case = 100*(int(request_data[0]['Cases'])-int(request_data[0]['Deceased']))/int(request_data[0]['Cases'])
		
		#  deceased = 100*(Deceased/Cases)
		deceased = 100*(int(request_data[0]['Deceased'])/int(request_data[0]['Cases']))
		sizes = [case, deceased]
		explode = (0, 0.1)
		
		plt.ioff()
		fig1, ax1 = plt.subplots()
		ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
				shadow=True, startangle=90)
		ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
		ax1.legend(loc='upper left',fancybox=True)
		ax1.set_title(str(request_data[0]['County']) + " County, " + str(request_data[0]['State']) + " - Ratio of Confirmed to Deceased")

		# save and return
		from io import BytesIO
		buf = BytesIO()
		plt.savefig(buf, transparent = True, format="png")
		buf_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
	return buf_base64

def generateStackPlot(request):
	# Stackplot chart, where the slices will be ordered and plotted counter-clockwise:
	# make a square figure and axes

	#First, retrieve data
	sql = """SELECT monthname(cft.last_update) as Month_part, STcountyFIPS as FIPS, cft.county,  cft.province_state as state, cft.confirmed as Cases, cft.deaths as Deceased
		FROM covidtraveler_db.covid_finalmaster_table cft inner join covidtraveler_db.US_ZIP_FIPS uzf
		on cft.FIPS = uzf.STcountyFIPS
		where dayofmonth(cft.last_update)=1
		and uzf.zip = %s
		order by STcountyFIPS, cft.last_update; """

	request_data = retrieveDBdata(request,sql)  

	# get unique list of months returned from query 
	#month_part = [d['Month_part'] for d in request_data if 'Month_part' in d]
	months = [d['Month_part'] for d in request_data if 'Month_part' in d]
	print("1-months=",months)
	# reduce list of month_part values to unique set (becomes a dictionary)
	months=set(months)
	# print("2-months=",months)
	# convert the dictionary back to a list structure
	months=list(months)
	print("3-months=",months)
	
	# get unique set of FIPS - will be used to filter data for each graph
	FIPS = [d['FIPS'] for d in request_data if 'FIPS' in d]
	# reduce list of FIPS values to unique set (becomes a dictionary)
	FIPS=set(FIPS)
	# convert the dictionary back to a list structure
	FIPS=list(FIPS)
	for i in FIPS:
		print("FIPS=",i)
	
	# start new row list that will contain only the FIPS to be graphed - this currently constrains to the first FIPS found, but the next revision will produce all
	row_list=list()
	for item in request_data:
		if item['FIPS'] == FIPS[0]:
			row_list.append(item)
	cases = [d['Cases'] for d in row_list if 'Cases' in d]
	deceased = [d['Deceased'] for d in row_list if 'Deceased' in d]

	# get unique name of county - will be used in display literals
	county = [d['county'] for d in row_list if 'county' in d]
	# reduce list of FIPS values to unique set (becomes a dictionary)
	county=set(county)
	# convert the dictionary back to a list structure
	county=list(county)

	# get unique name of state - will be used in display literals
	state = [d['state'] for d in row_list if 'state' in d]
	# reduce list of FIPS values to unique set (becomes a dictionary)
	state=set(state)
	# convert the dictionary back to a list structure
	state=list(state)

	population = {
		'Cases': cases,
		'Deceased': deceased,
	}
	plt.ioff()
	fig, ax = plt.subplots()
	ax.stackplot(months, population.values(),
				labels=population.keys())
	ax.legend(loc='upper left',fancybox=True)
	ax.set_title(county[0] + ' County, '+ state[0] + ' - FIPS ' + FIPS[0] + ' - Monthly Growth')
	ax.set_xlabel('Month')
	ax.set_ylabel('Population Affected')
	ax.facecolor = 'inherit'
	# save and return
	from io import BytesIO
	buf = BytesIO()
	#plt.savefig(buf, transparent=True, format="jpg")
	plt.savefig(buf, transparent=True, format="png")
	buf_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
	return buf_base64

def retrieveDBdata(request,sql):
	"""
	Uses request.POST.get("zipCode")).values() to get value of zip code to use as param for query 
	"""
	from django.db import connection
	data = request.POST.get("zipCode")
	
	with connection.cursor() as cursor:
		cursor.execute(sql, [data])
	return  dictFetchRows(cursor)

def dictFetchRows(cursor):
	"Return all rows from a cursor as a list of dictionaries"
	columns = [col[0] for col in cursor.description]
	print ("columns=",columns,"rows=",cursor.rowcount)
	result_list=list()
	rowcnt=0 	
	for row in cursor:
		res=dict()
		for i in range(len(columns)):
			key=columns[i]
			res[key] = row[i] 
		result_list.append(res)
	#print ("result_list=",result_list)
	return result_list
