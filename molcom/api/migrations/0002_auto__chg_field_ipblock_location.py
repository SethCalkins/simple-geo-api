# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'IpBlock.location'
        db.alter_column(u'api_ipblock', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.CityLocation'], null=True))

    def backwards(self, orm):

        # Changing field 'IpBlock.location'
        db.alter_column(u'api_ipblock', 'location_id', self.gf('django.db.models.fields.related.ForeignKey')(default=-1, to=orm['api.CityLocation']))

    models = {
        u'api.citylocation': {
            'Meta': {'object_name': 'CityLocation'},
            'area_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            'id': ('django.db.models.fields.IntegerField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'locality': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'metro_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'region_code': ('django.db.models.fields.CharField', [], {'max_length': '10'})
        },
        u'api.ipblock': {
            'Meta': {'unique_together': "(('ip_start', 'source'),)", 'object_name': 'IpBlock'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_end': ('django.db.models.fields.IntegerField', [], {}),
            'ip_start': ('django.db.models.fields.IntegerField', [], {}),
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.CityLocation']", 'null': 'True'}),
            'source': ('django.db.models.fields.IntegerField', [], {})
        },
        u'api.iplog': {
            'Meta': {'object_name': 'IpLog'},
            'ip': ('django.db.models.fields.GenericIPAddressField', [], {'max_length': '39', 'primary_key': 'True'}),
            'ip_block': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.IpBlock']", 'null': 'True'})
        },
        u'api.postalcode': {
            'Meta': {'unique_together': "(('country', 'postal_code'),)", 'object_name': 'PostalCode'},
            'city': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'api.recipe': {
            'Meta': {'object_name': 'Recipe'},
            'definition': ('django.db.models.fields.CharField', [], {'max_length': '4000'}),
            'id': ('django.db.models.fields.CharField', [], {'default': "'8100238a-94d5-4c51-b341-a5de8248549e'", 'max_length': '36', 'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']"})
        },
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Group']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'related_name': "u'user_set'", 'blank': 'True', 'to': u"orm['auth.Permission']"}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['api']