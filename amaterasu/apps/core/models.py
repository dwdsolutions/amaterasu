import datetime
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save


class Mailbox(models.Model):
    username = models.EmailField(max_length=150)
    password = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    maildir = models.CharField(max_length=150)
    quota = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    local_part = models.CharField(max_length=100)
    domain = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def clean(self):
        mailparts = self.username.split('@')
        self.local_part = mailparts[0]
        self.domain = mailparts[1]
        self.maildir = self.username + '/'
    
    def __unicode__(self):
        return "%s" % self.username
        
class Alias(models.Model):
    address = models.EmailField(max_length=150)
    goto = models.EmailField(max_length=150)
    domain = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return "%s" % self.address
        
class Domain(models.Model):
    name = models.CharField(max_length=100)
    transport = models.CharField(max_length=50, default='virtual')
    
    def __unicode__(self):
        return "%s" % self.name
        
@receiver(post_save, sender=Mailbox)        
def add_alias_and_transport(sender, **kwargs):
    if kwargs.get('created', False):
        mailbox = kwargs.get('instance', None)
        if mailbox:
            alias = Alias(address=mailbox.username, goto=mailbox.username, domain=mailbox.domain)
            alias.save()
            domain = Domain(name=mailbox.domain)
            domain.save()
