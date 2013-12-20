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
            ('latitute', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
            ('longitude', self.gf('django.db.models.fields.DecimalField')(max_digits=13, decimal_places=10)),
        ))
        db.send_create_signal(u'api', ['PostalCode'])

        # Adding unique constraint on 'PostalCode', fields ['country', 'postal_code']
        db.create_unique(u'api_postalcode', ['country', 'postal_code'])


    def backwards(self, orm):
        # Removing unique constraint on 'PostalCode', fields ['country', 'postal_code']
        db.delete_unique(u'api_postalcode', ['country', 'postal_code'])

        # Deleting model 'PostalCode'
        db.delete_table(u'api_postalcode')


    models = {
        u'api.postalcode': {
            'Meta': {'unique_together': "(('country', 'postal_code'),)", 'object_name': 'PostalCode'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitute': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['api']