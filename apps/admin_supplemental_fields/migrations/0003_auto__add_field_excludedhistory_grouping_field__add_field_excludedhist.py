# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'ExcludedHistory', fields ['model_pk']
        db.delete_unique(u'admin_supplemental_fields_excludedhistory', ['model_pk'])

        # Adding field 'ExcludedHistory.grouping_field'
        db.add_column(u'admin_supplemental_fields_excludedhistory', 'grouping_field',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)

        # Adding field 'ExcludedHistory.grouping_pk'
        db.add_column(u'admin_supplemental_fields_excludedhistory', 'grouping_pk',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True, blank=True),
                      keep_default=False)


        # Changing field 'ExcludedHistory.model_pk'
        db.alter_column(u'admin_supplemental_fields_excludedhistory', 'model_pk', self.gf('django.db.models.fields.CharField')(max_length=36, null=True))

        # Changing field 'ExcludedHistory.group'
        db.alter_column(u'admin_supplemental_fields_excludedhistory', 'group', self.gf('django.db.models.fields.CharField')(max_length=50, null=True))

    def backwards(self, orm):
        # Deleting field 'ExcludedHistory.grouping_field'
        db.delete_column(u'admin_supplemental_fields_excludedhistory', 'grouping_field')

        # Deleting field 'ExcludedHistory.grouping_pk'
        db.delete_column(u'admin_supplemental_fields_excludedhistory', 'grouping_pk')


        # User chose to not deal with backwards NULL issues for 'ExcludedHistory.model_pk'
        raise RuntimeError("Cannot reverse this migration. 'ExcludedHistory.model_pk' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'ExcludedHistory.model_pk'
        db.alter_column(u'admin_supplemental_fields_excludedhistory', 'model_pk', self.gf('django.db.models.fields.CharField')(max_length=36, unique=True))
        # Adding unique constraint on 'ExcludedHistory', fields ['model_pk']
        db.create_unique(u'admin_supplemental_fields_excludedhistory', ['model_pk'])


        # User chose to not deal with backwards NULL issues for 'ExcludedHistory.group'
        raise RuntimeError("Cannot reverse this migration. 'ExcludedHistory.group' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'ExcludedHistory.group'
        db.alter_column(u'admin_supplemental_fields_excludedhistory', 'group', self.gf('django.db.models.fields.CharField')(max_length=50))

    models = {
        'admin_supplemental_fields.excludedhistory': {
            'Meta': {'object_name': 'ExcludedHistory'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'excluded_fields': ('django.db.models.fields.TextField', [], {}),
            'group': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'grouping_field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'grouping_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'model_pk': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'object_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'admin_supplemental_fields.group': {
            'Meta': {'object_name': 'Group'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '5'}),
            'probability': ('django.db.models.fields.FloatField', [], {}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'admin_supplemental_fields.testsupplemental': {
            'Meta': {'object_name': 'TestSupplemental'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'f1': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'f2': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'f3': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'f4': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'f5': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['admin_supplemental_fields']