import datetime
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password


class Mailbox(models.Model):
    username = models.EmailField(max_length=150)
    password = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    maildir = models.CharField(max_length=150, blank=True)
    quota = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    local_part = models.CharField(max_length=100, blank=True)
    domain = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def clean(self):
        mailparts = self.username.split('@')
        self.local_part = mailparts[0]
        self.domain = mailparts[1]
        self.maildir = self.username + '/'
        self.password = make_password(password=self.password, hasher='md5')
    
    def __unicode__(self):
        return "%s" % self.username
        
    class Meta:
        verbose_name_plural = 'Mailboxes'
        
class Alias(models.Model):
    address = models.EmailField(max_length=150)
    goto = models.EmailField(max_length=150)
    domain = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return "%s" % self.address
        
    class Meta:
        verbose_name_plural = 'Aliases'
        
class Domain(models.Model):
    name = models.CharField(max_length=100)
    transport = models.CharField(max_length=50, default='virtual')
    active = models.BooleanField(default=True)
    
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

class PdnsDomains(models.Model):
    name = models.CharField(max_length=250)
    master = models.CharField(max_length=128, blank=True, null=True)
    last_check = models.IntegerField(blank=True, null=True)
    type = models.CharField(max_length=6)
    notified_serial = models.IntegerField(blank=True, null=True)
    account = models.CharField(max_length=40, blank=True, null=True)
    
    def __unicode__(self):
        return "%s" % self.name
        
    class Meta:
        verbose_name_plural = 'PDNS Domains'
        
class Records(models.Model):
    domain = models.ForeignKey(PdnsDomains, blank=True, null=True)
    name = models.CharField(max_length=255,  blank=True, null=True)
    type = models.CharField(max_length=10, blank=True, null=True)
    content = models.CharField(max_length=65535, blank=True, null=True)
    ttl = models.IntegerField(blank=True, null=True)
    prio = models.IntegerField(blank=True, null=True)
    change_date = models.IntegerField(blank=True, null=True)
    #ordername = models.CharField(max_length=255)
    #auth = models.BooleanField()
    
    def __unicode__(self):
        return "%s" % self.name
        
    class Meta:
        verbose_name_plural = 'Records'
        
class Supermasters(models.Model):
    ip = models.IPAddressField()
    nameserver = models.CharField(max_length=255)
    account = models.CharField(max_length=40)
