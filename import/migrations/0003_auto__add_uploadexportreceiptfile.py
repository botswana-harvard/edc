# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UploadExportReceiptFile'
        db.create_table(u'import_uploadexportreceiptfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('export_receipt_file', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
            ('file_name', self.gf('django.db.models.fields.CharField')(max_length=50, unique=True, null=True)),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('object_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('accepted', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('total', self.gf('django.db.models.fields.IntegerField')(default=0)),
            ('errors', self.gf('django.db.models.fields.TextField')()),
            ('receipt_datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('import', ['UploadExportReceiptFile'])


    def backwards(self, orm):
        # Deleting model 'UploadExportReceiptFile'
        db.delete_table(u'import_uploadexportreceiptfile')


    models = {
        'import.uploadexportreceiptfile': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'UploadExportReceiptFile'},
            'accepted': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'errors': ('django.db.models.fields.TextField', [], {}),
            'export_receipt_file': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'object_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'receipt_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'total': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'import.uploadtransactionfile': {
            'Meta': {'ordering': "('-created',)", 'object_name': 'UploadTransactionFile'},
            'consume': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'consumed': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'file_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'unique': 'True', 'null': 'True'}),
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