# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'UploadTransactionFile', fields ['file_date']
        db.delete_unique(u'import_uploadtransactionfile', ['file_date'])


    def backwards(self, orm):
        # Adding unique constraint on 'UploadTransactionFile', fields ['file_date']
        db.create_unique(u'import_uploadtransactionfile', ['file_date'])


    models = {
        'import.uploadexportreceiptfile': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'UploadExportReceiptFile'},
            'accepted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'duplicate': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'errors': ('django.db.models.fields.TextField', [], {'null': 'True'}),
            'export_receipt_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'object_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'receipt_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'import.uploadskipdays': {
            'Meta': {'ordering': "('-created',)", 'unique_together': "(('skip_date', 'identifier'),)", 'object_name': 'UploadSkipDays'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'skip_date': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 11, 12, 0, 0)'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'import.uploadtransactionfile': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'UploadTransactionFile'},
            'consume': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'consumed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'file_date': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'not_consumed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'producer': ('django.db.models.fields.TextField', [], {'max_length': '1000', 'null': 'True'}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'transaction_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['import']