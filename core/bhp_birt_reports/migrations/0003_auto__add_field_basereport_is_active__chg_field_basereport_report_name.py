# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Removing unique constraint on 'BaseReport', fields ['report_name']
        db.delete_unique(u'bhp_birt_reports_basereport', ['report_name'])

        # Adding field 'BaseReport.is_active'
        db.add_column(u'bhp_birt_reports_basereport', 'is_active',
                      self.gf('django.db.models.fields.BooleanField')(default=False),
                      keep_default=False)


        # Changing field 'BaseReport.report_name'
        db.alter_column(u'bhp_birt_reports_basereport', 'report_name', self.gf('django.db.models.fields.CharField')(max_length=150))

    def backwards(self, orm):
        # Deleting field 'BaseReport.is_active'
        db.delete_column(u'bhp_birt_reports_basereport', 'is_active')


        # Changing field 'BaseReport.report_name'
        db.alter_column(u'bhp_birt_reports_basereport', 'report_name', self.gf('django.db.models.fields.CharField')(max_length=25, unique=True))
        # Adding unique constraint on 'BaseReport', fields ['report_name']
        db.create_unique(u'bhp_birt_reports_basereport', ['report_name'])


    models = {
        'bhp_birt_reports.basereport': {
            'Meta': {'object_name': 'BaseReport'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_name': ('django.db.models.fields.CharField', [], {'max_length': '150'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'bhp_birt_reports.reportparameter': {
            'Meta': {'unique_together': "(('report', 'parameter_name'),)", 'object_name': 'ReportParameter'},
            'app_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'One.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_selectfield': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'parameter_name': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'parameter_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'query_string': ('django.db.models.fields.CharField', [], {'max_length': '200', 'null': 'True', 'blank': 'True'}),
            'report': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_birt_reports.BaseReport']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['bhp_birt_reports']