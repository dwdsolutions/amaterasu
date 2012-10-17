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
from django.http import HttpResponseRedirect
from pprint import pprint
from models import Plan, ClientProfile, Domain, Mailbox, Records
from forms import ClientProfileForm, DomainForm, MailboxForm, RecordForm

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
    
    def get_success_url(self):
        return reverse('index')
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.client = self.request.user
        self.object.save()
        return super(DomainAddView, self).form_valid(form)
        
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
    paginate_by = 25
    
    def get_queryset(self):
        return Mailbox.objects.filter(domain=self.kwargs.get('domain_id'))
        
    def get_context_data(self, **kwargs):
        context = super(EmailListView, self).get_context_data(**kwargs)
        context['domain_id'] = self.kwargs.get('domain_id')
        
        return context
        
class EmailAddView(CreateView):
    model = Mailbox
    form_class = MailboxForm
    template_name = "add_email.html"
    
    def get_success_url(self):
        return reverse("email-index", args=[self.kwargs.get('domain_id')])
        
    def form_valid(self, form):
        self.object = form.save(commit=False)
        domain = Domain.objects.get(pk=self.kwargs.get('domain_id'))
        self.object.domain = domain
        self.object.save()
        return super(EmailAddView, self).form_valid(form)
        
class EmailEditView(UpdateView):
    model = Mailbox
    form_class = MailboxForm
    template_name = "edit_email.html"
    
    def get_success_url(self):
        return reverse("email-index", args=[self.object.domain.id])
        
class EmailDisableView(View):
    """
    Class to change the status from a mailbox to disable
    """
    def get(self, request, *args, **kwargs):
        email = Mailbox.objects.get(pk=kwargs.get('email_id'))
        email.active = False
        email.save()
        
        return HttpResponseRedirect(reverse('email-index', args=[kwargs.get('domain_id')]))
        
class EmailEnableView(View):
    """
    Class to change the status from a mailbox to disable
    """
    def get(self, request, *args, **kwargs):
        email = Mailbox.objects.get(pk=kwargs.get('email_id'))
        email.active = True
        email.save()
        
        return HttpResponseRedirect(reverse('email-index', args=[kwargs.get('domain_id')]))
        
class DNSRecordListView(ListView):
    """
    Show the DNS records for one domain
    """
    model = Records
    context_object_name = "records"
    template_name = "domain_records_list.html"
    
    def get_queryset(self):
        return Record.objects.filter(domain=self.kwargs.get('domain_id'))
        
    def get_context_data(self, **kwargs):
        context = super(DNSRecordListView, self).get_context_data(**kwargs)
        context['domain_id'] = self.kwargs.get('domain_id')
        
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
