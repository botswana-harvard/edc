# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'UploadFile'
        db.create_table(u'import_uploadfile', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('file_path', self.gf('django.db.models.fields.FilePathField')(max_length=100)),
            ('file_name', self.gf('django.db.models.fields.files.FileField')(max_length=100)),
        ))
        db.send_create_signal('import', ['UploadFile'])


    def backwards(self, orm):
        # Deleting model 'UploadFile'
        db.delete_table(u'import_uploadfile')


    models = {
        'import.uploadfile': {
            'Meta': {'object_name': 'UploadFile'},
            'file_name': ('django.db.models.fields.files.FileField', [], {'max_length': '100'}),
            'file_path': ('django.db.models.fields.FilePathField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'})
        }
    }

    complete_apps = ['import']