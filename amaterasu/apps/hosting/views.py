from django.views.generic import FormView, TemplateView, ListView, DetailView, UpdateView, RedirectView, UpdateView
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
from core.models import ClientProfile

class HostingIndexView(TemplateView):
    template_name = "hosting/index.html"
    
    def get_context_data(self, **kwargs):
        context = super(HostingIndexView, self).get_context_data(**kwargs)
        context['hosting_active'] = True
        
        return context
        
    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(HostingIndexView, self).dispatch(*args, **kwargs)
        
class HostingListEmailView(ListView):
    model = ClientProfile
    template_name = 'hosting/index.html'