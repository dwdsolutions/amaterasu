from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from views import HostingIndexView

urlpatterns = patterns('',
    url(r'^$', HostingIndexView.as_view(), name="hosting-index"),
    
)