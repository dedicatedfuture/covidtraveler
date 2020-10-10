# Generated by Django 3.1.1 on 2020-10-08 04:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='CovidFinalmasterTable',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fips', models.FloatField(blank=True, db_column='FIPS', null=True)),
                ('county', models.CharField(blank=True, max_length=255, null=True)),
                ('province_state', models.CharField(blank=True, max_length=255, null=True)),
                ('country_region', models.CharField(blank=True, max_length=255, null=True)),
                ('last_update', models.DateField(blank=True, null=True)),
                ('lat', models.FloatField(blank=True, null=True)),
                ('long_field', models.FloatField(blank=True, db_column='long_', null=True)),
                ('confirmed', models.FloatField(blank=True, null=True)),
                ('deaths', models.FloatField(blank=True, null=True)),
                ('recovered', models.FloatField(blank=True, null=True)),
                ('active_case', models.FloatField(blank=True, null=True)),
                ('daily_confirmed_case', models.FloatField(blank=True, null=True)),
                ('daily_deaths_case', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'covid_finalmaster_table',
                'managed': False,
            },
        ),
        migrations.CreateModel(
            name='UsZipFips',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('zip', models.CharField(blank=True, max_length=255, null=True)),
                ('countyname', models.CharField(blank=True, db_column='CountyName', max_length=255, null=True)),
                ('state', models.CharField(blank=True, db_column='State', max_length=255, null=True)),
                ('stcountyfips', models.CharField(blank=True, db_column='STcountyFIPS', max_length=255, null=True)),
            ],
            options={
                'db_table': 'US_ZIP_FIPS',
                'managed': False,
            },
        ),
        migrations.DeleteModel(
            name='RecentNewsArticles',
        ),
    ]
