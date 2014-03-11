# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'Application'
        db.create_table(u'barrow_application', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=255)),
            ('display_name', self.gf('django.db.models.fields.CharField')(max_length=255)),
        ))
        db.send_create_signal(u'barrow', ['Application'])

        # Adding model 'Spider'
        db.create_table(u'barrow_spider', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('application', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['barrow.Application'])),
            ('name', self.gf('django.db.models.fields.CharField')(default=u'Default Spider', max_length=255)),
            ('config', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'barrow', ['Spider'])

        # Adding model 'SpiderTask'
        db.create_table(u'barrow_spidertask', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spider', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['barrow.Spider'])),
            ('start_time', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True)),
            ('end_time', self.gf('django.db.models.fields.DateTimeField')(default=None, null=True, blank=True)),
            ('state', self.gf('django.db.models.fields.IntegerField')(default=0)),
        ))
        db.send_create_signal(u'barrow', ['SpiderTask'])

        # Adding model 'SpiderResult'
        db.create_table(u'barrow_spiderresult', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('spider_task', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['barrow.SpiderTask'])),
            ('hash_value', self.gf('django.db.models.fields.CharField')(max_length=256)),
            ('content', self.gf('django.db.models.fields.TextField')()),
        ))
        db.send_create_signal(u'barrow', ['SpiderResult'])


    def backwards(self, orm):
        # Deleting model 'Application'
        db.delete_table(u'barrow_application')

        # Deleting model 'Spider'
        db.delete_table(u'barrow_spider')

        # Deleting model 'SpiderTask'
        db.delete_table(u'barrow_spidertask')

        # Deleting model 'SpiderResult'
        db.delete_table(u'barrow_spiderresult')


    models = {
        u'barrow.application': {
            'Meta': {'object_name': 'Application'},
            'display_name': ('django.db.models.fields.CharField', [], {'max_length': '255'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '255'})
        },
        u'barrow.spider': {
            'Meta': {'object_name': 'Spider'},
            'application': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['barrow.Application']"}),
            'config': ('django.db.models.fields.TextField', [], {}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u'Default Spider'", 'max_length': '255'})
        },
        u'barrow.spiderresult': {
            'Meta': {'object_name': 'SpiderResult'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'hash_value': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spider_task': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['barrow.SpiderTask']"})
        },
        u'barrow.spidertask': {
            'Meta': {'object_name': 'SpiderTask'},
            'end_time': ('django.db.models.fields.DateTimeField', [], {'default': 'None', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'spider': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['barrow.Spider']"}),
            'start_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'blank': 'True'}),
            'state': ('django.db.models.fields.IntegerField', [], {'default': '0'})
        }
    }

    complete_apps = ['barrow']