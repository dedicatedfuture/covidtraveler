# Generated by Django 3.1.1 on 2020-10-16 01:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pages', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='StateConfirmedDeceasedTotal',
            fields=[
                ('province_state', models.CharField(blank=True, max_length=255, primary_key=True, serialize=False, unique=True)),
                ('confirmed_total', models.FloatField(blank=True, null=True)),
                ('deceased_total', models.FloatField(blank=True, null=True)),
            ],
            options={
                'db_table': 'vw_state_confirmed_deceased_total',
                'managed': False,
            },
        ),
    ]
