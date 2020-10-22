from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('contactus/', views.contactus, name='contactus'),
    path('news/', views.news, name='news'),
    path('about/', views.about, name='about'),
    path('us_states/', views.us_states, name='us_states'),
    path('', views.showStates, name="showStates")
]