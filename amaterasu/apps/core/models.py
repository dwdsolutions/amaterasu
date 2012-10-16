import re
import time
import datetime
from django.db import models
from django.conf import settings
from django.utils.translation import ugettext as _
from django.contrib.auth.models import User
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.hashers import make_password
from passlib.hash import md5_crypt


class Domain(models.Model):
    """
    Class to represent an email domain
    """
    name = models.CharField(max_length=100)
    transport = models.CharField(max_length=50, default='dovecot')
    client = models.ForeignKey(User)
    have_dns_service = models.BooleanField(default=True)
    active = models.BooleanField(default=True)
    
    def __unicode__(self):
        return "{0}".format(self.name)

class Mailbox(models.Model):
    """
    Class to represent a mailbox
    """
    domain = models.ForeignKey(Domain)
    username = models.EmailField(max_length=150, unique=True)
    password = models.CharField(max_length=250)
    name = models.CharField(max_length=250)
    maildir = models.CharField(max_length=150, blank=True)
    quota = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    local_part = models.CharField(max_length=100, blank=True)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Mailboxes'
        
    def __unicode__(self):
        return '{}'.format(self.username)
    
    def clean(self):
        res = ''
        mailparts = self.username.split('@')
        self.local_part = mailparts[0]
        #self.domain = mailparts[1]
        self.maildir = self.username + '/'
        
        res = re.search(r"\$1\$", self.password)
        if not res:
            self.password = md5_crypt.encrypt(self.password)
        
class Alias(models.Model):
    """
    Class to represent an email alias
    """
    address = models.EmailField(max_length=150)
    goto = models.TextField(max_length=150)
    domain = models.CharField(max_length=100)
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name_plural = 'Aliases'
    
    def __unicode__(self):
        return "{0}".format(self.address)
        
@receiver(post_save, sender=Mailbox)        
def add_alias_and_transport(sender, **kwargs):
    if kwargs.get('created', False):
        mailbox = kwargs.get('instance', None)
        if mailbox:
            alias = Alias(address=mailbox.username, goto=mailbox.username, domain=mailbox.domain)
            alias.save()
            domain = mailbox.domain
            if domain.transport != 'dovecot':
                domain.transport = 'dovecot'
                domain.save()
            else:
                domain.save()
                
@receiver(post_save, sender=Domain)
def create_pdns_domain(sender, **kwargs):
    """
    Create the PDNS Domain if have_dns_service is active in Domain model
    """
    if kwargs.get('created', False):
        domain = kwargs.get('instance', None)
        if domain.have_dns_service:
            pdns_domain = PdnsDomains(name=domain.name, type="MASTER", notified_serial=int(time.time()))

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
    
    class Meta:
        verbose_name_plural = 'PDNS Domains'
    
    def __unicode__(self):
        return "{0}".format(self.name)
        
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
    # This is for add support for dns sec. But not now.
    #ordername = models.CharField(max_length=255)
    #auth = models.BooleanField()
    
    class Meta:
        verbose_name_plural = 'Records'
    
    def __unicode__(self):
        return "{}".format(self.name)
        
class Supermasters(models.Model):
    ip = models.IPAddressField()
    nameserver = models.CharField(max_length=255)
    account = models.CharField(max_length=40)
    
    def __unicode__(self):
        return "{0}".format(self.nameserver)
    
# Class related to plans and clients
class Language(models.Model):
    """
    Class to represent the languages support for every client
    """
    name = models.CharField(max_length=100)
    
    class Meta:
        ordering = ['id']
    
    def __unicode__(self):
        return "{}".format(self.name)


class Plan(models.Model):
    name = models.CharField(max_length=150)
    bandwidth = models.DecimalField(_("Bandwidth MB"), max_digits=10, decimal_places=2, default=5096)
    disk_space = models.DecimalField(_("Disk Space MB"), max_digits=10, decimal_places=2, default=300)
    email_accounts = models.IntegerField(default=10)
    ftp_accounts = models.IntegerField(default=5)
    languages = models.ManyToManyField(Language)
    db_mysql = models.IntegerField()
    db_postgres = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    
    def __unicode__(self):
        return "{}".format(self.name)
    
    
class ClientProfile(models.Model):
    user = models.OneToOneField(User)
    phone = models.CharField(max_length=15)
    
    class Meta:
        ordering = ['user']
        verbose_name = 'Client'
        verbose_name_plural = 'Clients'
        
    def __unicode__(self):
        return '{0}'.format(self.get_full_name())
        
    def get_full_name(self):
        return '{0} {1}'.format(self.user.first_name, self.user.last_name)
        
    get_full_name.verbose_name = "Full Name"
