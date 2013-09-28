# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'CriteriaAudit'
        db.create_table('bhp_eligibility_criteria_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('reference_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('criteria', self.gf('django.db.models.fields.TextField')(max_length=35)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('bhp_eligibility', ['CriteriaAudit'])

        # Adding model 'Criteria'
        db.create_table('bhp_eligibility_criteria', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=45)),
            ('reference_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('criteria', self.gf('django.db.models.fields.TextField')(max_length=35)),
        ))
        db.send_create_signal('bhp_eligibility', ['Criteria'])


    def backwards(self, orm):
        # Deleting model 'CriteriaAudit'
        db.delete_table('bhp_eligibility_criteria_audit')

        # Deleting model 'Criteria'
        db.delete_table('bhp_eligibility_criteria')


    models = {
        'bhp_eligibility.criteria': {
            'Meta': {'object_name': 'Criteria'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'criteria': ('django.db.models.fields.TextField', [], {'max_length': '35'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reference_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        },
        'bhp_eligibility.criteriaaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'CriteriaAudit', 'db_table': "'bhp_eligibility_criteria_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'criteria': ('django.db.models.fields.TextField', [], {'max_length': '35'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '45'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reference_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250'})
        }
    }

    complete_apps = ['bhp_eligibility']