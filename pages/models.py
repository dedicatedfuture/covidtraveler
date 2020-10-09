from django.db import models


class UsZipFips(models.Model):
    zip = models.CharField(max_length=255, blank=True, null=True)
    countyname = models.CharField(db_column='CountyName', max_length=255, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=255, blank=True, null=True)  # Field name made lowercase.
    stcountyfips = models.CharField(db_column='STcountyFIPS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'US_ZIP_FIPS'

class UsZipFipsV2(models.Model):
    zip = models.CharField(max_length=255)
    countyname = models.CharField(db_column='CountyName', max_length=255)  # Field name made lowercase.
    state = models.CharField(db_column='State', max_length=255)  # Field name made lowercase.
    stcountyfips = models.CharField(db_column='STcountyFIPS', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'US_ZIP_FIPS_v2'


class CovidFinalmasterTable(models.Model):
    fips = models.FloatField(db_column='FIPS', blank=True, null=True)  # Field name made lowercase.
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
