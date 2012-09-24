from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from views import HostingIndexView, DomainEditView

urlpatterns = patterns('',
    url(r'^$', HostingIndexView.as_view(), name="hosting-index"),
    url(r'^/domain/(?P<pk>\d+)/edit/$', DomainEditView.as_view(), name="edit-domain"),
)