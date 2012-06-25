import uuid
import logging
import datetime
from django.views.generic import FormView, TemplateView, ListView, DetailView, UpdateView, RedirectView
from django.views.generic.base import View
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.shortcuts import render_to_response, get_object_or_404, get_list_or_404
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth.models import User
from django.contrib.auth import logout
from pprint import pprint
from models import Plan

class IndexView(TemplateView):
    """
    Show the index dashboard
    """
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['index_active'] = True
        
        return context
    
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(IndexView, self).dispatch(*args, **kwargs)
        
class RedirectToIndexView(RedirectView):
    """
    Redirect to index after logout
    """
    def get_redirect_url(self, **kwargs):
        logout(self.request)
        return reverse('index')
        
class HostingView(ListView):
    model = Plan
    template_name = "plan_list.html"
    
    def get_context_data(self, **kwargs):
        context = super(HostingView, self).get_context_data(**kwargs)
        context['hosting_active'] = True
        
        return context
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HostingView, self).dispatch(*args, **kwargs)
    
