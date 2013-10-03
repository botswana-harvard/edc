# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'IdentifierSequence'
        db.create_table('ph_dispenser_identifiersequence', (
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('device_id', self.gf('django.db.models.fields.IntegerField')(default=99)),
        ))
        db.send_create_signal('ph_dispenser', ['IdentifierSequence'])



    def backwards(self, orm):
        # Deleting model 'IdentifierSequence'
        db.delete_table('ph_dispenser_identifiersequence')


    models = {
        'bhp_registration.registeredsubject': {
            'Meta': {'ordering': "['subject_identifier']", 'unique_together': "(('first_name', 'dob', 'initials'),)", 'object_name': 'RegisteredSubject'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'randomization_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_identifier': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'relative_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'screening_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']", 'null': 'True', 'blank': 'True'}),
            'subject_consent_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'undetermined'", 'max_length': '25', 'null': 'True'}),
            'survival_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_variables.studysite': {
            'Meta': {'ordering': "['site_code']", 'unique_together': "[('site_code', 'site_name')]", 'object_name': 'StudySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'site_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'site_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'ph_dispenser.dispensing': {
            'Meta': {'object_name': 'Dispensing'},
            'copies': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dispense_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 5, 28, 0, 0)'}),
            'dose': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'packing_amount': ('django.db.models.fields.IntegerField', [], {}),
            'packing_unit': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_registration.RegisteredSubject']", 'null': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '36'}),
            'is_derived': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'padding': ('django.db.models.fields.IntegerField', [], {'default': '4'}),
            'sequence_app_label': ('django.db.models.fields.CharField', [], {'default': "'bhp_identifier'", 'max_length': '50'}),
            'sequence_model_name': ('django.db.models.fields.CharField', [], {'default': "'sequence'", 'max_length': '50'}),
            'sequence_number': ('django.db.models.fields.IntegerField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'ph_dispenser.identifiersequence': {
            'Meta': {'object_name': 'IdentifierSequence'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {'default': '99'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['ph_dispenser']