from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . request import Request
import feedparser, matplotlib.pyplot as plt, base64
from io import StringIO, BytesIO
from PIL import Image
from matplotlib.patches import Shadow
from django.db import connection
from . forms import ZipCodeForm, ContactUsForm
import feedparser

	# Create your views here.
def index(request):

	# if user enters input, this code will fire because of the POST action by the user clicking Submit
	if request.method == 'POST':
		img2=img1="data:image/png;base64,"
		req = Request(request)
		print("index()#1 request.method=",request.method, "req.state=",req.state)

		#data sanity check - if data available for request then prepare search_results page
		if isDataAvailableForRequest(req):
			img1+=generatePieGraphic(req)
			img2+=generateStackPlot(req)
			print("index()#2 request.method=",request.method, "req.state=",req.state)
			img3, img4 = generateDualPlotCases(req)
			msg_text = getMessagesForRequest(req)
			if msg_text == None:
				msg_text = ''
			context = {'graph1': img1, 'graph2': img2, 'graph3' : img3, 'graph4' : img4, 'msg_text': msg_text, 'current_state' : req.state}
			return render(request, "pages/search_results.html", context)		
		else:	#populate error page
			err_msg = 'No data found for zipcode ' + req.zip 
			context = {'err_msg': err_msg}
			return render(request, 'pages/errorpage.html', context)
	
	else: # home page was just invoked, so initialize the form and render
		# this code renders the form that gets user input
		req = Request(request)
		print("index() request.method=",request.method, "req=",req)
		form = ZipCodeForm(req) 
		context={'form': form}		
		return render(request, 'base.html', context)

def isDataAvailableForRequest(req):
	sql="""
	SELECT count(*) as RowCnt
	FROM covidtraveler_db.covid_finalmaster_table
	WHERE fips IN 
	(SELECT distinct STcountyFIPS 
	FROM covidtraveler_db.US_ZIP_FIPS 
	WHERE zip = %s);
	"""
	result = retrieveDBdata2(req,sql,req.ZIPCODE)
	print ("isDataAvailableForRequest() result=",result, " count=",result[0]['RowCnt'])
	if (result[0]['RowCnt'] >0 ):
		return True
	else:
		return False

def get_county(request):
	from django.http import JsonResponse
	if request.method =='POST' and request.is_ajax():
		req = Request(request)
		form = ZipCodeForm(req)
		retval = form.getCountyChoicesAsDict(req)
		print("get_county() retval1=",retval)
		return JsonResponse(retval, safe=False)
		#return JsonResponse({'countyChoice': 'Sussex'})	# this is a hard coded response to test returning data to the ajax response
		

def errorpage(request):
	return render(request, 'pages/errorpage.html')

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

def retrieveDBdata(req,sql):
	"""
	Uses Request object to determine the type of request is being processed - this controls how the parameters are passed to the sql 
	"""
	from django.db import connection

	with connection.cursor() as cursor:
		if req.search_type() == req.ZIPCODE:
			cursor.execute(sql, [req.zip])
		elif req.search_type() == req.STATE_COUNTY:		
			data = [req.county,req.state]
			cursor.execute(sql, data)
		elif req.search_type() == req.STATE_ONLY:		
			data = [req.state]
			cursor.execute(sql, data)		
		elif req.search_type() == req.COUNTY_ONLY:		
			data = [req.county]
			cursor.execute(sql, data)		
		else:
			cursor.execute(sql)
		print("retrieveDBdata() req.search_type()=",req.search_type(), "=sql=",sql )
	return  dictFetchRows(cursor)

def retrieveDBdata2(req,sql,reqType):
	"""
	... 
	"""
	from django.db import connection

	if reqType == req.ZIPCODE:
		data = req.zip
	elif reqType in (req.STATE_COUNTY, req.STATE_ONLY):
		data = req.state
	elif reqType == req.COUNTY_ONLY:
		data = req._county_
	else:	# just execute the SQL, no params
		print ("retrieveDBdata2 data=None, sql=",sql)
		with connection.cursor() as cursor:
			cursor.execute(sql)
		return dictFetchRows(cursor)
	print("retrieveDBdata2() data=",data, "sql=",sql)
	with connection.cursor() as cursor:
		cursor.execute(sql, [data])
	return  dictFetchRows(cursor)

def dictFetchRows(cursor):
	"""
	Return all rows from cursor as a list of dictionaries
	"""
	columns = [col[0] for col in cursor.description]
	print ("columns=",columns,"rows=",cursor.rowcount)
	result_list=list()
	for row in cursor:
		res=dict()
		for i in range(len(columns)):
			key=columns[i]
			res[key] = row[i] 
		result_list.append(res)
	return result_list

def getMessagesForRequest(req):
	"""
	Returns any messages for the request - these are maintained in the database.
	"""
	if req.search_type()==req.ZIPCODE:
		sql="""
		select distinctrow zm.zipcode, mt.msg_text 
		from zips_msgs zm
		inner join msg_text mt on zm.msg_id = mt.msg_id
		where zm.zipcode = %s;
		"""
		print("getMessagesForRequest() here")
		request_data = retrieveDBdata2(req,sql,req.ZIPCODE)
		#print("getMessagesForRequest() request_data(zip)=",request_data)
		msg = [d.get('msg_text', None) for d in request_data]
		if msg!=None:
			if len(msg)>0:
				# get list of counties where the zip code exists
				retVal = msg[0] + " Counties that contain zipcode " + req._zip_ + " include : " + getCountyListForZipcode(req) 
				return retVal
			else:
				return None
		else:
			return None

	else: # defaulting to a county name search 
		sql="""
		select fc.county_name, fc.fips, mt.msg_text 
		from fips_county fc
		inner join fips_msgs fm on fm.fips = fc.fips
		inner join msg_text mt on mt.msg_id = fm.msg_id
		where fc.county_name = %s
		"""
		request_data = retrieveDBdata2(req,sql,req.COUNTY_ONLY)
		print("getMessagesForRequest() request_data(county)=",request_data)

def getCountyListForZipcode(req):
	"""
	Obtain unique list of counties for zip code passed in the Request object
	"""
	sql="""
	SELECT distinct CountyName FROM covidtraveler_db.US_ZIP_FIPS
	where zip = %s;
	"""
	county_list = retrieveDBdata2(req,sql,req.ZIPCODE)
	county_names = [d.get('CountyName', None) for d in county_list]
	if county_names!=None:
		return str(county_names)
	else:
		return None

def generatePieGraphic(request):
	# Pie chart, where the slices will be ordered and plotted counter-clockwise:
	# make a square figure and axes

	if request.search_type()==request.ZIPCODE:
		sql = """
			SELECT uzf.STcountyFIPS AS FIPS, cft.county AS County, cft.province_state AS State,
			SUM(cft.daily_confirmed_case) AS Cases, SUM(cft.daily_deaths_case) AS Deceased 
			FROM covid_finalmaster_table cft JOIN US_ZIP_FIPS uzf ON ((cft.FIPS = uzf.STcountyFIPS)) 
			WHERE uzf.zip = %s 
			GROUP BY uzf.STcountyFIPS , cft.county , cft.province_state 
			"""
	if request.search_type()==request.STATE_COUNTY:
		sql = """
			SELECT uzf.STcountyFIPS AS FIPS, cft.county AS County, cft.province_state AS State,
			SUM(cft.daily_confirmed_case) AS Cases, SUM(cft.daily_deaths_case) AS Deceased
			FROM covid_finalmaster_table cft JOIN US_ZIP_FIPS uzf ON ((cft.FIPS = uzf.STcountyFIPS))
			WHERE uzf.CountyName = %s
			and uzf.State = %s
			GROUP BY uzf.STcountyFIPS , cft.county , cft.province_state;
			"""

	request_data = retrieveDBdata(request,sql) 
	print("generatePieGraphic SQL=",sql)
	print("request_data=",request_data)

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
	else:
		buf_base64 = None
	return buf_base64

def generateStackPlot(request):
	# Stackplot chart, where the slices will be ordered and plotted counter-clockwise:
	# make a square figure and axes

	#First, retrieve data
	if request.search_type()==request.ZIPCODE:
		sql = """SELECT monthname(cft.last_update) as Month_part, STcountyFIPS as FIPS, cft.county,  cft.province_state as state, cft.confirmed as Cases, cft.deaths as Deceased
			FROM covidtraveler_db.covid_finalmaster_table cft inner join covidtraveler_db.US_ZIP_FIPS uzf
			on cft.FIPS = uzf.STcountyFIPS
			where dayofmonth(cft.last_update)=1
			and uzf.zip = %s
			order by STcountyFIPS, cft.last_update; """
	if request.search_type()==request.STATE_COUNTY:
		sql = """SELECT monthname(cft.last_update) as Month_part, cft.FIPS, cft.county,  cft.province_state as state, cft.confirmed as Cases, cft.deaths as Deceased
			FROM covidtraveler_db.covid_finalmaster_table cft 
			where dayofmonth(cft.last_update)=1
			and cft.county = %s
			and cft.province_state = %s
			order by cft.FIPS, cft.last_update; """

	#print("generateStackPlot sql=",sql)
	request_data = retrieveDBdata(request,sql)  
	if len(request_data) > 0:
		# get list of months returned from query - if more than one row returned there will be dupe month names
		months = [d['Month_part'] for d in request_data if 'Month_part' in d]
		# remove dupe month names from list
		months = list(dict.fromkeys(months))
		
		# get unique set of FIPS - will be used to filter data for each graph
		FIPS = [d['FIPS'] for d in request_data if 'FIPS' in d]
		# reduce list of FIPS values to unique set (becomes a dictionary)
		FIPS=list(dict.fromkeys(FIPS))
		for i in FIPS:
			print("FIPS=",i)
		
		# start new row list that will contain only the FIPS to be graphed - this currently constrains to the first FIPS found, and
		# msg text will be provided explaining to the user that they need to search additional counties within the state for more information
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

		#!!!fugly code alert!!!
		request.state = state #this is a fudge - should not need this here!!
		#!!!fugly code alert!!!

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
		plt.savefig(buf, transparent=True, format="png")
		buf_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
	else:
		buf_base64 = ''
	return buf_base64

def generateDualPlotCases(req):
	# Dual plot chart to compare two related data items that occur with different scaling
	import numpy as np
	#First, retrieve query data from request
	print("generateDualPlotCases() here")

	if req.search_type()==req.ZIPCODE:
		sql = """
			SELECT cft.province_state as state, cft.FIPS, cft.county, cft.last_update as event_day, 
				cft.daily_confirmed_case as Cases, cft.daily_deaths_case as Deceased
			FROM covidtraveler_db.covid_finalmaster_table cft inner join covidtraveler_db.US_ZIP_FIPS uzf
			ON cft.FIPS = uzf.STcountyFIPS
			where cft.last_update between date_sub(curdate(), INTERVAL 30 DAY) and curdate()
			and uzf.zip = %s
			order by cft.FIPS, cft.last_update
		"""	
	elif req.search_type()==req.STATE_COUNTY:
		sql = """
			SELECT cft.province_state as state, cft.FIPS, cft.county, cft.last_update as event_day, 
				cft.daily_confirmed_case as Cases, cft.daily_deaths_case as Deceased
			FROM covidtraveler_db.covid_finalmaster_table cft 
			WHERE cft.county = %s
			AND cft.province_state = %s
			order by cft.FIPS, cft.last_update
		"""	
	#print("generateDualPlotCases sql=", sql)
	county_data = retrieveDBdata(req,sql)

	sql = """
		SELECT cft.province_state as state, cft.last_update as event_day, sum(cft.daily_confirmed_case) as Cases, sum(cft.daily_deaths_case) as Deceased
		FROM covidtraveler_db.covid_finalmaster_table cft 
		where cft.last_update between date_sub(curdate(), INTERVAL 30 DAY) and curdate()
		and cft.province_state = %s
		group by cft.province_state, cft.last_update;
	"""
	state_data = retrieveDBdata2(req,sql,req.STATE_ONLY)
	#state_data = retrieveDBdata(req,sql)
	if len(county_data) > 0 and len(state_data) > 0:
		from io import BytesIO
		
		# get list of months returned from query - if more than one row returned there will be dupe month names
		dates = [d['event_day'] for d in county_data if 'event_day' in d]
		# remove dupe dates from list
		dates = list(dict.fromkeys(dates))
		# days 
		days = len(dates)

		# get unique set of FIPS - will be used to filter data for each graph
		FIPS = [d['FIPS'] for d in county_data if 'FIPS' in d]
		# reduce list of FIPS values to unique set (becomes a dictionary)
		FIPS=list(dict.fromkeys(FIPS))
		for i in FIPS:
			print("FIPS=",i)
		
		# start new row list that will contain only the FIPS to be graphed - this currently constrains to the first FIPS found, and
		# msg text will be provided explaining to the user that they need to search additional counties within the state for more information
		row_list=list()
		for item in county_data:
			if item['FIPS'] == FIPS[0]:
				row_list.append(item)
		county_cases = [d['Cases'] for d in row_list if 'Cases' in d]
		county_cases_min=min(county_cases)
		county_cases_max=max(county_cases)
		county_deceased = [d['Deceased'] for d in row_list if 'Deceased' in d]
		county_deceased_min=min(county_deceased)
		county_deceased_max=max(county_deceased)
		#print("county_cases_min=",county_cases_min,"county_cases_max=",county_cases_max,"county_cases=",county_cases)

		# get unique name of county - will be used in display literals
		county = [d['county'] for d in row_list if 'county' in d]
		# reduce list of FIPS values to unique set (becomes a dictionary)
		county=set(county)
		# convert the dictionary back to a list structure
		county=list(county)

		# begin adjacent subplots image
		t = np.arange(0, days, 1)

		# s1 is county 
		#s1 = county_cases

		# s2 is state data
		state_cases = [d['Cases'] for d in state_data if 'Cases' in d]
		state_cases_min=min(state_cases)
		state_cases_max=max(state_cases)
		state_deceased = [d['Deceased'] for d in state_data if 'Deceased' in d]
		state_deceased_min=min(state_deceased)
		state_deceased_max=max(state_deceased)
		print("state_deceased_min=",state_deceased_min,"state_deceased_max=",state_deceased_max,"state_deceased=",state_deceased)
		
		# cases graphs
		plt.ioff()	
		fig_cases, axs_cases = plt.subplots(2, 1, sharex=True)
		# Remove horizontal space between axes
		fig_cases.subplots_adjust(hspace=0)

		# Plot each graph, and manually set the y tick values
		axs_cases[0].plot(t, county_cases)
		axs_cases[0].set_yticks(np.arange(county_cases_min, county_cases_max, ((county_cases_max-county_cases_min)//10)))
		axs_cases[0].set_ylim(county_cases_min, county_cases_max*1.1)

		axs_cases[1].plot(t, state_cases)
		axs_cases[1].set_yticks(np.arange(state_cases_min, state_cases_max, (state_cases_max-state_cases_min)//10))
		axs_cases[1].set_ylim(state_cases_min, state_cases_max*1.1)

		label=county[0]+' County'
		axs_cases[0].set_ylabel(label)
		label= 'Past '+ str(days) +' Days'
		axs_cases[1].set_xlabel(label)
		label=str(req.state)
		axs_cases[1].set_ylabel(label)
		axs_cases[0].legend(loc='upper left',fancybox=True)
		axs_cases[0].set_title(county[0] + ' County vs. '+ str(req.state) + ' - Daily New Cases')
		buf = BytesIO()
		plt.savefig(buf, transparent=True, format="png")
		cases_graph = "data:image/png;base64,"
		cases_graph += base64.b64encode(buf.getvalue()).decode('utf-8')

		#--- deceased graphs ---
		fig_deceased, axs_deceased = plt.subplots(2, 1, sharex=True)
		# Remove horizontal space between axes
		plt.ioff()
		fig_deceased.subplots_adjust(hspace=0)

		# Plot each graph, and manually set the y tick values
		axs_deceased[0].plot(t, county_deceased)
		if (county_deceased_max-county_deceased_min)<10:
				ticks=.5
		else:
				ticks=1
		axs_deceased[0].set_yticks(np.arange(county_deceased_min, county_deceased_max, ((county_deceased_max-county_deceased_min)//ticks)))
		print("county_deceased_min=",county_deceased_min,"county_deceased_max=",county_deceased_max,"ticks=",ticks)
		axs_deceased[0].set_ylim(county_deceased_min, county_deceased_max*1.1)

		axs_deceased[1].plot(t, state_deceased)
		axs_deceased[1].set_yticks(np.arange(state_deceased_min, state_deceased_max, (state_deceased_max-state_deceased_min)//10))
		axs_deceased[1].set_ylim(state_deceased_min, state_deceased_max*1.1)

		label=county[0]+' County'
		axs_deceased[0].set_ylabel(label)
		label= 'Past '+ str(days) +' Days'
		axs_deceased[1].set_xlabel(label)
		label=str(req.state)
		axs_deceased[1].set_ylabel(label)
		axs_deceased[0].legend(loc='upper left',fancybox=True)
		axs_deceased[0].set_title(county[0] + ' County vs. '+ str(req.state) + ' - Daily Deceased')
		buf = BytesIO()
		plt.savefig(buf, transparent=True, format="png")
		deceased_graph = "data:image/png;base64,"
		deceased_graph += base64.b64encode(buf.getvalue()).decode('utf-8')
		# end adjacent subplots image

	else:
		cases_graph = ''
		deceased_graph = ''
	return cases_graph, deceased_graph


