
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
	path('', views.index, name='index'),
	path('search/', views.search, name='search'),
	path('addurl/', views.crawler, name='crawler'),
	path('insert/', views.addUrl, name='insert'),
	path('crawl/', views.crawl, name='crawl')
]