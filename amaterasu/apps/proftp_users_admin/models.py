import hashlib
import base64
import re
from django.db import models

# Create your models here.
class Usuario(models.Model):
    userid = models.CharField(max_length=32)
    password = models.CharField(max_length=45)
    uid = models.SmallIntegerField(default=5500)
    gid = models.SmallIntegerField(default=5500)
    homedir = models.CharField(max_length=255)
    shell = models.CharField(max_length=20, default="/sbin/nologin")
    count = models.IntegerField(default=0)
    accessed = models.DateTimeField()
    modified = models.DateTimeField()
    
    def __unicode__(self):
        return unicode(self.userid)
    
    def _encrypt_password(self):
        '''
        Encripta el password en formato md5
        '''
        search = re.search("{md5}", self.password)
        if not search:
            self.password = "{md5}"+base64.b64encode(hashlib.md5(self.password).digest())
        
    def save(self, *args, **kargs):
        '''
        Reescribe el metodo save para encriptar el password antes de guardar.
        '''
        self._encrypt_password()
        super(Usuario, self).save(*args, **kargs)
    
class Group(models.Model):
    group_name = models.CharField(max_length=16)
    gid = models.SmallIntegerField(default=5500)
    members = models.CharField(max_length=16)
    
    def __unicode__(self):
        return unicode(self.group_name)
    
class Quota_Limit(models.Model):
    '''
    Tabla con los limites de quota por usuario
    '''
    
    ENUM = (
        (u'user', u'Usuario'),
        (u'group', u'Grupo'),
        (u'class', u'Clase'),
        (u'all', u'Todos'),
    )
    
    BOOLEAN = (
        (u'true', u'Si'),
        (u'false', u'No'),
    )
    
    LIMIT = (
        (u'soft', u'Flexible'),
        (u'hard', u'Estricto'),
    )
    
    name = models.CharField(max_length=30)
    quota_type = models.CharField(max_length=7, choices=ENUM, default="user")
    per_session = models.CharField(max_length=7, choices=BOOLEAN, default="false")
    limit_type = models.CharField(max_length=7, choices=LIMIT, default="soft")
    bytes_in_avail = models.FloatField(default=0)
    bytes_out_avail = models.FloatField(default=0)
    bytes_xfer_avail = models.FloatField(default=0)
    files_in_avail = models.IntegerField(default=0)
    files_out_avail = models.IntegerField(default=0)
    files_xfer_avail = models.IntegerField(default=0)
    
    def __unicode__(self):
        return unicode(self.name)
    
class Quota_Tally(models.Model):
    '''
    Tabla con los datos sobre las cuotas
    '''
    
    ENUM = (
        (u'user', u'Usuario'),
        (u'group', u'Grupo'),
        (u'class', u'Clase'),
        (u'all', u'Todos'),
    )
    
    name = models.CharField(max_length=30)
    quota_type = models.CharField(max_length=7, choices=ENUM, default="user")
    bytes_in_avail = models.FloatField(default=0)
    bytes_out_avail = models.FloatField(default=0)
    bytes_xfer_avail = models.FloatField(default=0)
    files_in_avail = models.IntegerField(default=0)
    files_out_avail = models.IntegerField(default=0)
    files_xfer_avail = models.IntegerField(default=0)
    
    def __unicode__(self):
        return unicode(self.name)