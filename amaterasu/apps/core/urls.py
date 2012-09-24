from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from views import IndexView, RedirectToIndexView, ProfileView, DomainEditView, DomainAddView

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', IndexView.as_view(), name="index"),
    url(r'^login/$', auth_views.login, {'template_name': 'auth/login.html'}, name="auth_login"),
    url(r'^logout/$', RedirectToIndexView.as_view(), name="auth_logout"),
    url(r'^hosting/', include('hosting.urls')),
    url(r'^domain/(?P<pk>\d+)/edit/$', DomainEditView.as_view(), name="edit-domain"),
    url(r'^domain/add/$', DomainAddView.as_view(), name="add-domain"),
    url(r'^profile/(?P<pk>\d+)/$', ProfileView.as_view(), name="profile"),
    url(r'^admin/', include(admin.site.urls)),
)