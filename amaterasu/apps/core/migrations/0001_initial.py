# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Mailbox'
        db.create_table('core_mailbox', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('username', self.gf('django.db.models.fields.EmailField')(max_length=150)),
            ('password', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('maildir', self.gf('django.db.models.fields.CharField')(max_length=150, blank=True)),
            ('quota', self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=10, decimal_places=2)),
            ('local_part', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100, blank=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('core', ['Mailbox'])

        # Adding model 'Alias'
        db.create_table('core_alias', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('address', self.gf('django.db.models.fields.EmailField')(max_length=150)),
            ('goto', self.gf('django.db.models.fields.EmailField')(max_length=150)),
            ('domain', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('core', ['Alias'])

        # Adding model 'Domain'
        db.create_table('core_domain', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('transport', self.gf('django.db.models.fields.CharField')(default='virtual', max_length=50)),
            ('active', self.gf('django.db.models.fields.BooleanField')(default=True)),
        ))
        db.send_create_signal('core', ['Domain'])

        # Adding model 'PdnsDomains'
        db.create_table('core_pdnsdomains', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250)),
            ('master', self.gf('django.db.models.fields.CharField')(max_length=128, null=True, blank=True)),
            ('last_check', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=6)),
            ('notified_serial', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('account', self.gf('django.db.models.fields.CharField')(max_length=40, null=True, blank=True)),
        ))
        db.send_create_signal('core', ['PdnsDomains'])

        # Adding model 'Records'
        db.create_table('core_records', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('domain', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['core.PdnsDomains'], null=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=255, null=True, blank=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('content', self.gf('django.db.models.fields.CharField')(max_length=65535, null=True, blank=True)),
            ('ttl', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('prio', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
            ('change_date', self.gf('django.db.models.fields.IntegerField')(null=True, blank=True)),
        ))
        db.send_create_signal('core', ['Records'])

        # Adding model 'Supermasters'
        db.create_table('core_supermasters', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip', self.gf('django.db.models.fields.IPAddressField')(max_length=15)),
            ('nameserver', self.gf('django.db.models.fields.CharField')(max_length=255)),
            ('account', self.gf('django.db.models.fields.CharField')(max_length=40)),
        ))
        db.send_create_signal('core', ['Supermasters'])


    def backwards(self, orm):
        # Deleting model 'Mailbox'
        db.delete_table('core_mailbox')

        # Deleting model 'Alias'
        db.delete_table('core_alias')

        # Deleting model 'Domain'
        db.delete_table('core_domain')

        # Deleting model 'PdnsDomains'
        db.delete_table('core_pdnsdomains')

        # Deleting model 'Records'
        db.delete_table('core_records')

        # Deleting model 'Supermasters'
        db.delete_table('core_supermasters')


    models = {
        'core.alias': {
            'Meta': {'object_name': 'Alias'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'address': ('django.db.models.fields.EmailField', [], {'max_length': '150'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'goto': ('django.db.models.fields.EmailField', [], {'max_length': '150'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'})
        },
        'core.domain': {
            'Meta': {'object_name': 'Domain'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'transport': ('django.db.models.fields.CharField', [], {'default': "'virtual'", 'max_length': '50'})
        },
        'core.mailbox': {
            'Meta': {'object_name': 'Mailbox'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'local_part': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'maildir': ('django.db.models.fields.CharField', [], {'max_length': '150', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'quota': ('django.db.models.fields.DecimalField', [], {'default': '0', 'max_digits': '10', 'decimal_places': '2'}),
            'username': ('django.db.models.fields.EmailField', [], {'max_length': '150'})
        },
        'core.pdnsdomains': {
            'Meta': {'object_name': 'PdnsDomains'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '40', 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'last_check': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'master': ('django.db.models.fields.CharField', [], {'max_length': '128', 'null': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'notified_serial': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '6'})
        },
        'core.records': {
            'Meta': {'object_name': 'Records'},
            'change_date': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'content': ('django.db.models.fields.CharField', [], {'max_length': '65535', 'null': 'True', 'blank': 'True'}),
            'domain': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['core.PdnsDomains']", 'null': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'null': 'True', 'blank': 'True'}),
            'prio': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'ttl': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'})
        },
        'core.supermasters': {
            'Meta': {'object_name': 'Supermasters'},
            'account': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip': ('django.db.models.fields.IPAddressField', [], {'max_length': '15'}),
            'nameserver': ('django.db.models.fields.CharField', [], {'max_length': '255'})
        }
    }

    complete_apps = ['core']