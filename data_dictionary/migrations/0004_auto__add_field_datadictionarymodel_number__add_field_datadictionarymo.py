# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DataDictionaryModel.number'
        db.add_column(u'data_dictionary_datadictionarymodel', 'number',
                      self.gf('django.db.models.fields.IntegerField')(null=True),
                      keep_default=False)

        # Adding field 'DataDictionaryModel.in_admin'
        db.add_column(u'data_dictionary_datadictionarymodel', 'in_admin',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DataDictionaryModel.number'
        db.delete_column(u'data_dictionary_datadictionarymodel', 'number')

        # Deleting field 'DataDictionaryModel.in_admin'
        db.delete_column(u'data_dictionary_datadictionarymodel', 'in_admin')


    models = {
        'data_dictionary.datadictionarymodel': {
            'Meta': {'object_name': 'DataDictionaryModel'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'blank': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'choices': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'db_field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'db_table': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'default': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'encrypted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'in_admin': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'max_length': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'null': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'number': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'primary_key': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prompt': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'unique': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['data_dictionary']