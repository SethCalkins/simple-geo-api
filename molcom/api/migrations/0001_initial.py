# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'PostalCode'
        db.create_table(u'api_postalcode', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('region', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('city', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
        ))
        db.send_create_signal(u'api', ['PostalCode'])

        # Adding unique constraint on 'PostalCode', fields ['country', 'postal_code']
        db.create_unique(u'api_postalcode', ['country', 'postal_code'])

        # Adding model 'Recipe'
        db.create_table(u'api_recipe', (
            ('id', self.gf('django.db.models.fields.CharField')(default='0fde47a2-c859-4b69-9171-2765310b2cb8', max_length=36, primary_key=True)),
            ('user', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['auth.User'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('definition', self.gf('django.db.models.fields.CharField')(max_length=4000)),
        ))
        db.send_create_signal(u'api', ['Recipe'])

        # Adding model 'CityLocation'
        db.create_table(u'api_citylocation', (
            ('id', self.gf('django.db.models.fields.IntegerField')(primary_key=True)),
            ('country', self.gf('django.db.models.fields.CharField')(max_length=2)),
            ('region_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('locality', self.gf('django.db.models.fields.CharField')(max_length=100)),
            ('postal_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('latitude', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
            ('metro_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('area_code', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal(u'api', ['CityLocation'])

        # Adding model 'IpBlock'
        db.create_table(u'api_ipblock', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('ip_start', self.gf('django.db.models.fields.IntegerField')()),
            ('ip_end', self.gf('django.db.models.fields.IntegerField')()),
            ('source', self.gf('django.db.models.fields.IntegerField')()),
            ('location', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.CityLocation'])),
        ))
        db.send_create_signal(u'api', ['IpBlock'])

        # Adding unique constraint on 'IpBlock', fields ['ip_start', 'source']
        db.create_unique(u'api_ipblock', ['ip_start', 'source'])

        # Adding model 'IpLog'
        db.create_table(u'api_iplog', (
            ('ip', self.gf('django.db.models.fields.GenericIPAddressField')(max_length=39, primary_key=True)),
            ('ip_block', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['api.IpBlock'], null=True)),
        ))
        db.send_create_signal(u'api', ['IpLog'])


    def backwards(self, orm):
        # Removing unique constraint on 'IpBlock', fields ['ip_start', 'source']
        db.delete_unique(u'api_ipblock', ['ip_start', 'source'])

        # Removing unique constraint on 'PostalCode', fields ['country', 'postal_code']
        db.delete_unique(u'api_postalcode', ['country', 'postal_code'])

        # Deleting model 'PostalCode'
        db.delete_table(u'api_postalcode')

        # Deleting model 'Recipe'
        db.delete_table(u'api_recipe')

        # Deleting model 'CityLocation'
        db.delete_table(u'api_citylocation')

        # Deleting model 'IpBlock'
        db.delete_table(u'api_ipblock')

        # Deleting model 'IpLog'
        db.delete_table(u'api_iplog')


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
            'location': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['api.CityLocation']"}),
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
            'id': ('django.db.models.fields.CharField', [], {'default': "'fe6c1901-fb4c-4664-9fca-27d021c366f2'", 'max_length': '36', 'primary_key': 'True'}),
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