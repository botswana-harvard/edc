# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'StudySpecific.revision'
        db.add_column(u'bhp_variables_studyspecific', 'revision',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'StudySite.revision'
        db.add_column(u'bhp_variables_studysite', 'revision',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'StudySpecific.revision'
        db.delete_column(u'bhp_variables_studyspecific', 'revision')

        # Deleting field 'StudySite.revision'
        db.delete_column(u'bhp_variables_studysite', 'revision')


    models = {
        'bhp_variables.studysite': {
            'Meta': {'ordering': "['site_code']", 'unique_together': "[('site_code', 'site_name')]", 'object_name': 'StudySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'site_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'site_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_variables.studyspecific': {
            'Meta': {'object_name': 'StudySpecific'},
            'age_at_adult_lower_bound': ('django.db.models.fields.IntegerField', [], {'default': '18'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'device_id': ('django.db.models.fields.IntegerField', [], {}),
            'gender_of_consent': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_prefix': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'machine_type': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '25'}),
            'maximum_age_of_consent': ('django.db.models.fields.IntegerField', [], {}),
            'minimum_age_of_consent': ('django.db.models.fields.IntegerField', [], {}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'protocol_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'protocol_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'protocol_title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '100'}),
            'research_title': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '250'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'study_start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier_modulus': ('django.db.models.fields.IntegerField', [], {'default': '7'}),
            'subject_identifier_prefix': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '3'}),
            'subject_identifier_seed': ('django.db.models.fields.IntegerField', [], {'default': '1000'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'default': "'subject'", 'max_length': '100'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bhp_variables']