import uuid
import logging
import datetime
from django.views.generic import FormView, TemplateView, ListView, DetailView, UpdateView, RedirectView, CreateView
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
from models import Plan, ClientProfile, Domain, Mailbox
from forms import ClientProfileForm, DomainForm

class IndexView(TemplateView):
    """
    Show the index dashboard
    """
    template_name = "index.html"
    
    def get_context_data(self, **kwargs):
        context = super(IndexView, self).get_context_data(**kwargs)
        context['index_active'] = True
        if self.request.user.is_superuser:
            context['domains'] = Domain.objects.all()
        else:
            context['domains'] = Domain.objects.filter(client=self.request.user)
        
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
        
class DomainAddView(CreateView):
    """
    Class based view to show the form to add a domain
    """
    model = Domain
    form_class = DomainForm
    template_name = "add_domain.html"
        
class DomainEditView(UpdateView):
    """
    Class based view to show the form to edit a domain
    """
    model = Domain
    form_class = DomainForm
    template_name = "edit_domain.html"
    
class EmailListView(ListView):
    model = Mailbox
    context_object_name = "mailboxes"
    template_name = "email_list.html"
    
    def get_context_data(self, **kwargs):
        """
        Create the context object for this view
        """
        context = super(EmailListView, self).get_context_data(**kwargs)
        context['mailboxes'] = Mailbox.objects.filter(domain=kwargs.get('domain_id'))
        
        return context
        
class ProfileView(UpdateView):
    """
    View to show the profile
    """
    model = ClientProfile
    form_class = ClientProfileForm
    template_name = "profile.html"
    
    def get_success_url(self):
        return reverse('profile', args=[self.request.user.id])
    
    def get_object(self, queryset=None):
        key = self.request.GET.get('pk')
        profile, created = ClientProfile.objects.get_or_create(user=self.request.user)
        return profile
