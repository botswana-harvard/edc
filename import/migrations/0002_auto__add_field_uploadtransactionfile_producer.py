# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'UploadTransactionFile.producer'
        db.add_column(u'import_uploadtransactionfile', 'producer',
                      self.gf('django.db.models.fields.TextField')(max_length=1000, null=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'UploadTransactionFile.producer'
        db.delete_column(u'import_uploadtransactionfile', 'producer')


    models = {
        'import.uploadtransactionfile': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'UploadTransactionFile'},
            'consume': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'consumed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
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