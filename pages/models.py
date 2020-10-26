from django.db import models



class UsZipFips(models.Model):
    ziptable_id = models.AutoField(db_column='ZipTable_id', unique=True,primary_key=True)  # Field name made lowercase.
    zip = models.CharField(max_length=255, blank=True, null=True)
    countyname = models.CharField(db_column='CountyName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stcountyfips = models.CharField(db_column='STcountyFIPS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'US_ZIP_FIPS'

class CovidFinalmasterTable(models.Model):
    id = models.AutoField(unique=True,primary_key=True)
    fips = models.CharField(db_column='FIPS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    county = models.CharField(max_length=255, blank=True, null=True)
    province_state = models.CharField(max_length=255, blank=True, null=True)
    country_region = models.CharField(max_length=255, blank=True, null=True)
    last_update = models.DateField(blank=True, null=True)
    lat = models.FloatField(blank=True, null=True)
    long_field = models.FloatField(db_column='long_', blank=True, null=True)  # Field renamed because it ended with '_'.
    confirmed = models.FloatField(blank=True, null=True)
    deaths = models.FloatField(blank=True, null=True)
    recovered = models.FloatField(blank=True, null=True)
    active_case = models.FloatField(blank=True, null=True)
    daily_confirmed_case = models.FloatField(blank=True, null=True)
    daily_deaths_case = models.FloatField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'covid_finalmaster_table'

class Feedback(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    body = models.TextField()

    class Meta:
        managed = False
        db_table = 'user_feedback'

