# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting field 'PostalCode.latitute'
        db.delete_column(u'api_postalcode', 'latitute')

        # Adding field 'PostalCode.latitude'
        db.add_column(u'api_postalcode', 'latitude',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=13, decimal_places=10),
                      keep_default=False)


    def backwards(self, orm):
        # Adding field 'PostalCode.latitute'
        db.add_column(u'api_postalcode', 'latitute',
                      self.gf('django.db.models.fields.DecimalField')(default=0, max_digits=13, decimal_places=10),
                      keep_default=False)

        # Deleting field 'PostalCode.latitude'
        db.delete_column(u'api_postalcode', 'latitude')


    models = {
        u'api.postalcode': {
            'Meta': {'unique_together': "(('country', 'postal_code'),)", 'object_name': 'PostalCode'},
            'country': ('django.db.models.fields.CharField', [], {'max_length': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'latitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'longitude': ('django.db.models.fields.DecimalField', [], {'max_digits': '13', 'decimal_places': '10'}),
            'postal_code': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'region': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['api']