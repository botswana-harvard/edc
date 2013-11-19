# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DataDictionaryModel'
        db.create_table(u'data_dictionary_datadictionarymodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('db_table', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('field', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('db_field', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('prompt', self.gf('django.db.models.fields.TextField')(null=True)),
            ('type', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('max_length', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('default', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('null', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('editable', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('help_text', self.gf('django.db.models.fields.CharField')(max_length=500, null=True)),
            ('encrypted', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('choices', self.gf('django.db.models.fields.TextField')(null=True)),
            ('primary_key', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('unique', self.gf('django.db.models.fields.BooleanField')(default=False)),
        ))
        db.send_create_signal('data_dictionary', ['DataDictionaryModel'])


    def backwards(self, orm):
        # Deleting model 'DataDictionaryModel'
        db.delete_table(u'data_dictionary_datadictionarymodel')


    models = {
        'data_dictionary.datadictionarymodel': {
            'Meta': {'object_name': 'DataDictionaryModel'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
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