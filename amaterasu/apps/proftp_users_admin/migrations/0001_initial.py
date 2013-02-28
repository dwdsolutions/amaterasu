# encoding: utf-8
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models

class Migration(SchemaMigration):

    def forwards(self, orm):
        
        # Adding model 'Usuario'
        db.create_table('proftp_users_admin_usuario', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('userid', self.gf('django.db.models.fields.CharField')(max_length=32)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('uid', self.gf('django.db.models.fields.SmallIntegerField')(default=5500)),
            ('gid', self.gf('django.db.models.fields.SmallIntegerField')(default=5500)),
            ('homedir', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('shell', self.gf('django.db.models.fields.CharField')(default='/sbin/nologin', max_length=20)),
            ('count', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('accessed', self.gf('django.db.models.fields.DateTimeField')()),
            ('modified', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('proftp_users_admin', ['Usuario'])

        # Adding model 'Group'
        db.create_table('proftp_users_admin_group', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('group_name', self.gf('django.db.models.fields.CharField')(max_length=16)),
            ('gid', self.gf('django.db.models.fields.SmallIntegerField')(default=5500)),
            ('members', self.gf('django.db.models.fields.CharField')(max_length=16)),
        ))
        db.send_create_signal('proftp_users_admin', ['Group'])

        # Adding model 'Quota_Limit'
        db.create_table('proftp_users_admin_quota_limit', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('quota_type', self.gf('django.db.models.fields.CharField')(default='user', max_length=7)),
            ('per_session', self.gf('django.db.models.fields.CharField')(default='false', max_length=7)),
            ('limit_type', self.gf('django.db.models.fields.CharField')(default='soft', max_length=7)),
            ('bytes_in_avail', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('bytes_out_avail', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('bytes_xfer_avail', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('files_in_avail', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('files_out_avail', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('files_xfer_avail', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('proftp_users_admin', ['Quota_Limit'])

        # Adding model 'Quota_Tally'
        db.create_table('proftp_users_admin_quota_tally', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('quota_type', self.gf('django.db.models.fields.CharField')(default='user', max_length=7)),
            ('bytes_in_avail', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('bytes_out_avail', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('bytes_xfer_avail', self.gf('django.db.models.fields.FloatField')(default=0)),
            ('files_in_avail', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('files_out_avail', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('files_xfer_avail', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal('proftp_users_admin', ['Quota_Tally'])


    def backwards(self, orm):
        
        # Deleting model 'Usuario'
        db.delete_table('proftp_users_admin_usuario')

        # Deleting model 'Group'
        db.delete_table('proftp_users_admin_group')

        # Deleting model 'Quota_Limit'
        db.delete_table('proftp_users_admin_quota_limit')

        # Deleting model 'Quota_Tally'
        db.delete_table('proftp_users_admin_quota_tally')


    models = {
        'proftp_users_admin.group': {
            'Meta': {'object_name': 'Group'},
            'gid': ('django.db.models.fields.SmallIntegerField', [], {'default': '5500'}),
            'group_name': ('django.db.models.fields.CharField', [], {'max_length': '16'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'members': ('django.db.models.fields.CharField', [], {'max_length': '16'})
        },
        'proftp_users_admin.quota_limit': {
            'Meta': {'object_name': 'Quota_Limit'},
            'bytes_in_avail': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'bytes_out_avail': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'bytes_xfer_avail': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'files_in_avail': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'files_out_avail': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'files_xfer_avail': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'limit_type': ('django.db.models.fields.CharField', [], {'default': "'soft'", 'max_length': '7'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'per_session': ('django.db.models.fields.CharField', [], {'default': "'false'", 'max_length': '7'}),
            'quota_type': ('django.db.models.fields.CharField', [], {'default': "'user'", 'max_length': '7'})
        },
        'proftp_users_admin.quota_tally': {
            'Meta': {'object_name': 'Quota_Tally'},
            'bytes_in_avail': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'bytes_out_avail': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'bytes_xfer_avail': ('django.db.models.fields.FloatField', [], {'default': '0'}),
            'files_in_avail': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'files_out_avail': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'files_xfer_avail': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'quota_type': ('django.db.models.fields.CharField', [], {'default': "'user'", 'max_length': '7'})
        },
        'proftp_users_admin.usuario': {
            'Meta': {'object_name': 'Usuario'},
            'accessed': ('django.db.models.fields.DateTimeField', [], {}),
            'count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'gid': ('django.db.models.fields.SmallIntegerField', [], {'default': '5500'}),
            'homedir': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'shell': ('django.db.models.fields.CharField', [], {'default': "'/sbin/nologin'", 'max_length': '20'}),
            'uid': ('django.db.models.fields.SmallIntegerField', [], {'default': '5500'}),
            'userid': ('django.db.models.fields.CharField', [], {'max_length': '32'})
        }
    }

    complete_apps = ['proftp_users_admin']
