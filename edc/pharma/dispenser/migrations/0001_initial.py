# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DispensingIdentifierModel'
        db.create_table('ph_dispenser_dispensingidentifiermodel', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=36)),
            ('padding', self.gf('django.db.models.fields.IntegerField')(default=4)),
        ))
        db.send_create_signal('ph_dispenser', ['DispensingIdentifierModel'])

        # Adding model 'Dispensing'
        db.create_table('ph_dispenser_dispensing', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('dispense_date', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2012, 9, 6, 0, 0))),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('sid', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('packing_amount', self.gf('django.db.models.fields.IntegerField')()),
            ('packing_unit', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('treatment', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('dose', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('copies', self.gf('django.db.models.fields.IntegerField')(default=1)),
        ))
        db.send_create_signal('ph_dispenser', ['Dispensing'])


    def backwards(self, orm):
        # Deleting model 'DispensingIdentifierModel'
        db.delete_table('ph_dispenser_dispensingidentifiermodel')

        # Deleting model 'Dispensing'
        db.delete_table('ph_dispenser_dispensing')


    models = {
        'ph_dispenser.dispensing': {
            'Meta': {'object_name': 'Dispensing'},
            'copies': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dispense_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2012, 9, 6, 0, 0)'}),
            'dose': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'packing_amount': ('django.db.models.fields.IntegerField', [], {}),
            'packing_unit': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'sid': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'treatment': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'ph_dispenser.dispensingidentifiermodel': {
            'Meta': {'ordering': "['-created']", 'object_name': 'DispensingIdentifierModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'padding': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['ph_dispenser']