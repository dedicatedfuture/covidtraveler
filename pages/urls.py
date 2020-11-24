from django.urls import path
from . import views

urlpatterns = [
	path('', views.index, name='index'),
    path('contactus/', views.contactus, name='contactus'),
    path('news/', views.news, name='news'),
    path('about/', views.about, name='about'),
    path('search_results/', views.search_results, name='search_results'),
    #path('get_county/', views.get_county, name='get_county'),
    path('errorpage/', views.errorpage, name='errorpage'),
]