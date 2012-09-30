from django.conf.urls import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    # url(r'^$', 'amaterasu.views.home', name='home'),
    url(r'^', include('core.urls')),
)
