import datetime
import re
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password
from passlib.hash import md5_crypt


class Mailbox(models.Model):
    """
    Class to represent a mailbox
    """
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
        res = ''
        mailparts = self.username.split('@')
        self.local_part = mailparts[0]
        self.domain = mailparts[1]
        self.maildir = self.username + '/'
        
        res = re.search("$1$", self.password)
        if not res:
            self.password = md5_crypt.encrypt(self.password)
    
    def __unicode__(self):
        return "%s" % self.username
        
    class Meta:
        verbose_name_plural = 'Mailboxes'
        
class Alias(models.Model):
    """
    Class to represent an email alias
    """
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
    """
    Class to represent an email domain
    """
    name = models.CharField(max_length=100)
    transport = models.CharField(max_length=50, default='dovecot')
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
            domain = Domain.objects.get_or_create(name=mailbox.domain)[0]
            if domain.transport != 'dovecot':
                domain.transport = 'dovecot'
                domain.save()

class PdnsDomains(models.Model):
    """
    Class to represent a DNS domain
    """
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
    """
    Class to store dns records from one domain in PDNS Domains
    """
    TYPES_OF_RECORDS = (
        ('SOA', 'SOA'),
        ('NS', 'NS'),
        ('MX', 'MX'),
        ('TXT', 'TXT'),
        ('PTR', 'PTR'),
        ('A', 'A'),
        ('AAAA', 'AAAA'),
        ('CNAME', 'CNAME'),
    )
    
    domain = models.ForeignKey(PdnsDomains, blank=True, null=True)
    name = models.CharField(max_length=255,  blank=True, null=True)
    type = models.CharField(choices=TYPES_OF_RECORDS, max_length=10, blank=True, null=True)
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
    
# Class related to plans and clients
class Language(models.Model):
    """
    Class to represent the languages support for every client
    """
    name = models.CharField(max_length=100)
    
    def __unicode__(self):
        return "%s" % self.name
        
    class Meta:
        ordering = ['id']

class Plan(models.Model):
    name = models.CharField(max_length=150)
    bandwidth = models.DecimalField(_("Bandwidth MB"), max_digits=10, decimal_places=2, default=5096)
    disk_space = models.DecimalField(_("Disk Space MB"), max_digits=10, decimal_places=2, default=300)
    email_accounts = models.IntegerField(default=10)
    ftp_accounts = models.IntegerField(default=5)
    languages = models.ManyToManyField(Language)
    db_mysql = models.IntegerField()
    db_postgres = models.IntegerField()
    
    def __unicode__(self):
        return "%s" % self.name
    
