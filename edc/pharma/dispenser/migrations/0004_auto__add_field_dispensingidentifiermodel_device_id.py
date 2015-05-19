# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Dispensing', fields ['user_modified']
        db.create_index('ph_dispenser_dispensing', ['user_modified'])

        # Adding index on 'Dispensing', fields ['user_created']
        db.create_index('ph_dispenser_dispensing', ['user_created'])

        # Adding field 'DispensingIdentifierModel.device_id'
        db.add_column('ph_dispenser_dispensingidentifiermodel', 'device_id',
                      self.gf('django.db.models.fields.IntegerField')(default=0),
                      keep_default=False)

        # Adding index on 'DispensingIdentifierModel', fields ['user_modified']
        db.create_index('ph_dispenser_dispensingidentifiermodel', ['user_modified'])

        # Adding index on 'DispensingIdentifierModel', fields ['user_created']
        db.create_index('ph_dispenser_dispensingidentifiermodel', ['user_created'])


    def backwards(self, orm):
        # Removing index on 'DispensingIdentifierModel', fields ['user_created']
        db.delete_index('ph_dispenser_dispensingidentifiermodel', ['user_created'])

        # Removing index on 'DispensingIdentifierModel', fields ['user_modified']
        db.delete_index('ph_dispenser_dispensingidentifiermodel', ['user_modified'])

        # Removing index on 'Dispensing', fields ['user_created']
        db.delete_index('ph_dispenser_dispensing', ['user_created'])

        # Removing index on 'Dispensing', fields ['user_modified']
        db.delete_index('ph_dispenser_dispensing', ['user_modified'])

        # Deleting field 'DispensingIdentifierModel.device_id'
        db.delete_column('ph_dispenser_dispensingidentifiermodel', 'device_id')


    models = {
        'ph_dispenser.dispensing': {
            'Meta': {'object_name': 'Dispensing'},
            'copies': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dispense_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 2, 20, 0, 0)'}),
            'dose': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'s007'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'s007'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'packing_amount': ('django.db.models.fields.IntegerField', [], {}),
            'packing_unit': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'sid': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'treatment': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'ph_dispenser.dispensingidentifiermodel': {
            'Meta': {'ordering': "['-created']", 'object_name': 'DispensingIdentifierModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'s007'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'s007'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'padding': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'sequence_number': ('django.db.models.fields.IntegerField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['ph_dispenser']