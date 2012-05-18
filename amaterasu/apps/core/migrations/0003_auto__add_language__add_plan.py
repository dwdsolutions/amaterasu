# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Language'
        db.create_table('core_language', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=100)),
        ))
        db.send_create_signal('core', ['Language'])

        # Adding model 'Plan'
        db.create_table('core_plan', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=150)),
            ('bandwidth', self.gf('django.db.models.fields.DecimalField')(default=5096, max_digits=10, decimal_places=2)),
            ('disk_space', self.gf('django.db.models.fields.DecimalField')(default=300, max_digits=10, decimal_places=2)),
            ('email_accounts', self.gf('django.db.models.fields.IntegerField')(default=10)),
            ('ftp_accounts', self.gf('django.db.models.fields.IntegerField')(default=5)),
            ('db_mysql', self.gf('django.db.models.fields.IntegerField')()),
            ('db_postgres', self.gf('django.db.models.fields.IntegerField')()),
        ))
        db.send_create_signal('core', ['Plan'])

        # Adding M2M table for field languages on 'Plan'
        db.create_table('core_plan_languages', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('plan', models.ForeignKey(orm['core.plan'], null=False)),
            ('language', models.ForeignKey(orm['core.language'], null=False))
        ))
        db.create_unique('core_plan_languages', ['plan_id', 'language_id'])


    def backwards(self, orm):
        # Deleting model 'Language'
        db.delete_table('core_language')

        # Deleting model 'Plan'
        db.delete_table('core_plan')

        # Removing M2M table for field languages on 'Plan'
        db.delete_table('core_plan_languages')


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
        'core.language': {
            'Meta': {'ordering': "['id']", 'object_name': 'Language'},
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
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
        'core.plan': {
            'Meta': {'object_name': 'Plan'},
            'bandwidth': ('django.db.models.fields.DecimalField', [], {'default': '5096', 'max_digits': '10', 'decimal_places': '2'}),
            'db_mysql': ('django.db.models.fields.IntegerField', [], {}),
            'db_postgres': ('django.db.models.fields.IntegerField', [], {}),
            'disk_space': ('django.db.models.fields.DecimalField', [], {'default': '300', 'max_digits': '10', 'decimal_places': '2'}),
            'email_accounts': ('django.db.models.fields.IntegerField', [], {'default': '10'}),
            'ftp_accounts': ('django.db.models.fields.IntegerField', [], {'default': '5'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'languages': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['core.Language']", 'symmetrical': 'False'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '150'})
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