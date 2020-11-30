"""! @brief COVID Traveler HTTP URLs Delegation"""
##
# @file urls.py
#
# @brief urls.py connects the http request processed by the django framework and hands off to handler code mapped to the calling URL.
#
# @section description_urls Description
# This file contains the URLs that map to the handlers for the respective user request. The urlpatterns struct is
# directly referenced by Django via the ROOT_URLCONF environment variable or by populating the settings.py file with
# ROOT_URLCONF set to the location of this file.
#
# @section description_urls Description
# Used to direct http requests to the appropriate application handler.
# - Sensor (base class)
# - TempSensor
#
## @section libraries_urls Libraries/Modules
# - Imports path from django.urls
# - Imports application functionality from package views.py
#
# @section author_urls Author(s)
# - Created by Team #3 on 11/28/2020.
# - Modified by Team #3 on 11/28/2020.
#
# Copyright (c) 2020 COVID Traveler Warning Team.  All rights reserved.

from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('contactus/', views.contactus, name='contactus'),
    path('news/', views.news, name='news'),
    path('about/', views.about, name='about'),
    #path('errorpage/', views.errorpage, name='errorpage'),
]