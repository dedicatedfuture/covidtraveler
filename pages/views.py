from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from . models import UsZipFips
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
		img1+=generatePieGraphic2(request)
		img2+=generateStackPlot(request)
		context = {'graph1': img1, 'graph2': img2, 'county1': '-- Montgomery --','county2': '-- Delaware --'}
		print("context=", context)	

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
	return render(request, 'pages/newsarticles.html', {
		'feed':feed
		})

def about(request):
	return render(request, 'pages/about.html')

def us_states(request):
	context = {
		'state': UsZipFips.state,
		'county': UsZipFips.countyname,
		'state': UsZipFips.state,
		'fips': UsZipFips.stcountyfips,
		'fips_list': UsZipFips.objects.all()[0:15],
	}
	return render(request, 'pages/us_states.html', context)

def search(request):
	form = ZipCodeForm()
	context={'form': form}
	if request.method == 'POST':
		context = {
		'zips_list': UsZipFips.objects.filter(zip=request.POST.get("zipCode")).values(),
		}	
	return render(request, 'pages/search.html', context)

def generatePieGraphic1(request):
	# Pie chart, where the slices will be ordered and plotted counter-clockwise:
	# make a square figure and axes

	#First, retrieve data
	#retrieveDBdata(request) ## has an issue 
	fig = plt.figure(figsize=(4, 4))
	ax = fig.add_axes([0.1, 0.1, 0.8, 0.8])

	labels = 'Cases', 'Deceased'
	case = 100*(12945-890)/12945
	deceased = 100*(890/12945)
	fracs = [case, deceased]

	#explode = (12945, 890, 12285, 762)
	explode = (0, 0.1)

	# We want to draw the shadow for each pie but we will not use "shadow"
	# option as it does'n save the references to the shadow patches.
	pies = ax.pie(fracs, explode=explode, labels=labels, autopct='%1.1f%%')

	for w in pies[0]:
		# set the id with the label.
		w.set_gid(w.get_label())

		# we don't want to draw the edge of the pie
		w.set_edgecolor("none")

	for w in pies[0]:
		# create shadow patch
		s = Shadow(w, -0.01, -0.01)
		s.set_gid(w.get_gid() + "_shadow")
		s.set_zorder(w.get_zorder() - 0.1)
		ax.add_patch(s)

	# save and return
	from io import BytesIO
	buf = BytesIO()
	plt.savefig(buf, format="jpg")
	#buf_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
	buf_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
	return buf_base64

def generatePieGraphic2(request):
	# Pie chart, where the slices will be ordered and plotted counter-clockwise:
	# make a square figure and axes
	req_dict = retrieveDBdata(request) ## has an issue
	labels = 'Cases', 'Deceased'
	case = 100*(12945-890)/12945
	deceased = 100*(890/12945)
	sizes = [case, deceased]

	#explode = (12945, 890, 12285, 762)
	explode = (0, 0.1)

	fig1, ax1 = plt.subplots()
	ax1.pie(sizes, explode=explode, labels=labels, autopct='%1.1f%%',
			shadow=True, startangle=90)
	ax1.axis('equal')  # Equal aspect ratio ensures that pie is drawn as a circle.
	ax1.legend(loc='upper left')
	ax1.set_title('Montgomery County - Ratio of Confirmed:Deceased')

	#plt.show()
	# save and return
	from io import BytesIO
	buf = BytesIO()
	plt.savefig(buf, format="jpg")
	buf_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
	return buf_base64

def generateStackPlot(request):
	# Stackplot chart, where the slices will be ordered and plotted counter-clockwise:
	# make a square figure and axes

	#First, retrieve data
	#retrieveDBdata(request) ## has an issue 
	months = ['May', 'June', 'July', 'August','September','October']
	confirmed = [4307, 7061, 8448, 9761, 11035, 12285]
	deceased = [351, 684, 801, 848, 861, 878]
	# year = [1950, 1960, 1970, 1980, 1990, 2000, 2010, 2018]
	population = {
		'Cases': [4307, 7061, 8448, 9761, 11035, 12285],
		'Deceased': [351, 684, 801, 848, 861, 878],
	}

	fig, ax = plt.subplots()
	ax.stackplot(months, population.values(),
				labels=population.keys())
	ax.legend(loc='upper left')
	ax.set_title('Montgomery County - Monthly Change')
	ax.set_xlabel('Month')
	ax.set_ylabel('People Affected')
	# save and return
	from io import BytesIO
	buf = BytesIO()
	plt.savefig(buf, format="jpg")
	#buf_base64 = base64.b64encode(buf.getvalue()).decode('utf-8').replace('\n', '')
	buf_base64 = base64.b64encode(buf.getvalue()).decode('utf-8')
	return buf_base64

def dictFetchAll(cursor):
    "Return all rows from a cursor as a dict"
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]

def retrieveDBdata(request):
	"""
	Uses request.POST.get("zipCode")).values() to get value of zip code to use as param for query 
	"""
	from django.db import connection
	sql = "SELECT uzf.zip AS zip, uzf.STcountyFIPS AS FIPS, cft.county AS county, cft.province_state AS state, "
	sql+= " SUM(cft.daily_confirmed_case) AS total_confirmed_cases, SUM(cft.daily_deaths_case) AS total_deceased "
	sql+= "FROM covid_finalmaster_table cft JOIN US_ZIP_FIPS uzf ON ((cft.FIPS = uzf.STcountyFIPS)))"
	sql+= "WHERE uzf.zip = %s "
	sql+= "GROUP BY uzf.zip , uzf.STcountyFIPS , cft.county , cft.province_state"
	print("sql=",sql)
	data = request.POST.get("zipCode")
	
	with connection.cursor() as cursor:
		#cursor.execute(sql, data)
		cursor.execute("SELECT uzf.zip AS zip, uzf.STcountyFIPS AS FIPS, cft.county AS county, cft.province_state AS state, SUM(cft.daily_confirmed_case) AS Total_confirmed_cases, SUM(cft.daily_deaths_case) AS total_deceased FROM (covid_finalmaster_table cft JOIN US_ZIP_FIPS uzf ON ((cft.FIPS = uzf.STcountyFIPS))) WHERE uzf.zip = %s GROUP BY uzf.zip , uzf.STcountyFIPS , cft.county , cft.province_state",[data])
	return dictFetchAll(cursor)

