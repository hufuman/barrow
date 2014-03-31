# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'Spider.last_update'
        db.add_column(u'barrow_spider', 'last_update',
                      self.gf('django.db.models.fields.DateTimeField')(auto_now=True, auto_now_add=True, default=datetime.datetime(2014, 3, 31, 0, 0), blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'Spider.last_update'
        db.delete_column(u'barrow_spider', 'last_update')


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
            'last_update': ('django.db.models.fields.DateTimeField', [], {'auto_now': 'True', 'auto_now_add': 'True', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'default': "u'Default Spider'", 'max_length': '255'}),
            'running': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        },
        u'barrow.spiderresult': {
            'Meta': {'object_name': 'SpiderResult'},
            'content': ('django.db.models.fields.TextField', [], {}),
            'create_time': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'null': 'True', 'blank': 'True'}),
            'hash_value': ('django.db.models.fields.CharField', [], {'max_length': '256'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'retrieved': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
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