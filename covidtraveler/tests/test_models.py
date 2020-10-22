from django.test import TestCase
from pages.models import UsZipFips, UsZipFipsV2, CovidFinalmasterTable, Feedback

class TestModels(TestCase):

	def setUp(self):
		self.usZipTest = UsZipFips(zip='19061', countyname='Delaware', state='PA', 
			stcountyfips='54321')
		self.usZipTesV2 = UsZipFipsV2(zip='19061', countyname='Delaware', state='PA', 
			stcountyfips='54321')
		self.covidFinalmasterTableTest = CovidFinalmasterTable(
				fips = '123',  
    			county = 'Philadelphia',
    			province_state = 'PA',
    			country_region = 'USA',
    			last_update = '10/1/20',
    			lat = '123',
   				long_field = '321',
   				confirmed = '10000',
    			deaths = '1000',
    			recovered = '9000',
    			active_case = '8000',
    			daily_confirmed_case = '1000',
    			daily_deaths_case = '100'
			)
		self.feedbackTest = Feedback(
			name = 'Bill',
    		email = 'Bill@bill.com',
    		body = 'Great website!'
    		)

	def test_UsZipFipsModel_Creation(self):
		entry = UsZipFips(zip='19061', countyname='Delaware', state='PA', 
			stcountyfips='54321')
		self.assertTrue(isinstance(entry, UsZipFips))
		self.assertEquals(self.usZipTest.zip, '19061')
		self.assertEquals(self.usZipTest.countyname, 'Delaware')
		
		




