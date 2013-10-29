# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):

        # Changing field 'ExportHistory.export_datetime'
        db.alter_column(u'export_exporthistory', 'export_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True))

    def backwards(self, orm):

        # User chose to not deal with backwards NULL issues for 'ExportHistory.export_datetime'
        raise RuntimeError("Cannot reverse this migration. 'ExportHistory.export_datetime' and its values cannot be restored.")
        
        # The following code is provided here to aid in writing a correct migration
        # Changing field 'ExportHistory.export_datetime'
        db.alter_column(u'export_exporthistory', 'export_datetime', self.gf('django.db.models.fields.DateTimeField')())

    models = {
        'export.exporthistory': {
            'Meta': {'object_name': 'ExportHistory'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'export_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'export_uuid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'exported': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'instance_pk': ('django.db.models.fields.CharField', [], {'max_length': '32'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'object_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'received': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'received_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'sent': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'sent_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'export.exporttest': {
            'Meta': {'object_name': 'ExportTest'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'f_char': ('django.db.models.fields.CharField', [], {'default': "'character'", 'max_length': '64'}),
            'f_choice': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '64'}),
            'f_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 10, 27, 0, 0)'}),
            'f_datetime': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 10, 27, 0, 0)'}),
            'f_integer': ('django.db.models.fields.IntegerField', [], {'default': '123'}),
            'f_text': ('django.db.models.fields.TextField', [], {'default': "'Space, the final frontier. These are the voyages of the starship enterprise'"}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'export.exporttransaction': {
            'Meta': {'ordering': "('-timestamp',)", 'object_name': 'ExportTransaction'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'change_type': ('django.db.models.fields.CharField', [], {'default': "'I'", 'max_length': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_error': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'is_ignored': ('django.db.models.fields.BooleanField', [], {'default': 'False', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'object_name': ('django.db.models.fields.CharField', [], {'max_length': '64', 'db_index': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '15'}),
            'timestamp': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'tx': ('django.db.models.fields.TextField', [], {}),
            'tx_pk': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['export']