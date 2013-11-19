# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'DataDictionaryModel.blank'
        db.add_column(u'data_dictionary_datadictionarymodel', 'blank',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'DataDictionaryModel.blank'
        db.delete_column(u'data_dictionary_datadictionarymodel', 'blank')


    models = {
        'data_dictionary.datadictionarymodel': {
            'Meta': {'object_name': 'DataDictionaryModel'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'blank': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'choices': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'db_field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'db_table': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'default': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'editable': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'encrypted': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'field': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'help_text': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'max_length': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'null': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'primary_key': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'prompt': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'type': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'unique': ('django.db.models.fields.BooleanField', [], {'default': 'False'})
        }
    }

    complete_apps = ['data_dictionary']