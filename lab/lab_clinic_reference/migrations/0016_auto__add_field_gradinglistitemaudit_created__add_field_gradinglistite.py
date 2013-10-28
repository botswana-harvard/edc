# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'GradingListItemAudit.created'
        db.add_column(u'lab_clinic_reference_gradinglistitem_audit', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'GradingListItemAudit.modified'
        db.add_column(u'lab_clinic_reference_gradinglistitem_audit', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'GradingListItemAudit.user_created'
        db.add_column(u'lab_clinic_reference_gradinglistitem_audit', 'user_created',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'GradingListItemAudit.user_modified'
        db.add_column(u'lab_clinic_reference_gradinglistitem_audit', 'user_modified',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'GradingListItemAudit.hostname_created'
        db.add_column(u'lab_clinic_reference_gradinglistitem_audit', 'hostname_created',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'GradingListItemAudit.hostname_modified'
        db.add_column(u'lab_clinic_reference_gradinglistitem_audit', 'hostname_modified',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeList.created'
        db.add_column(u'lab_clinic_reference_referencerangelist', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeList.modified'
        db.add_column(u'lab_clinic_reference_referencerangelist', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeList.user_created'
        db.add_column(u'lab_clinic_reference_referencerangelist', 'user_created',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeList.user_modified'
        db.add_column(u'lab_clinic_reference_referencerangelist', 'user_modified',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeList.hostname_created'
        db.add_column(u'lab_clinic_reference_referencerangelist', 'hostname_created',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeList.hostname_modified'
        db.add_column(u'lab_clinic_reference_referencerangelist', 'hostname_modified',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'GradingList.created'
        db.add_column(u'lab_clinic_reference_gradinglist', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'GradingList.modified'
        db.add_column(u'lab_clinic_reference_gradinglist', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'GradingList.user_created'
        db.add_column(u'lab_clinic_reference_gradinglist', 'user_created',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'GradingList.user_modified'
        db.add_column(u'lab_clinic_reference_gradinglist', 'user_modified',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'GradingList.hostname_created'
        db.add_column(u'lab_clinic_reference_gradinglist', 'hostname_created',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'GradingList.hostname_modified'
        db.add_column(u'lab_clinic_reference_gradinglist', 'hostname_modified',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItem.created'
        db.add_column(u'lab_clinic_reference_referencerangelistitem', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItem.modified'
        db.add_column(u'lab_clinic_reference_referencerangelistitem', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItem.user_created'
        db.add_column(u'lab_clinic_reference_referencerangelistitem', 'user_created',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItem.user_modified'
        db.add_column(u'lab_clinic_reference_referencerangelistitem', 'user_modified',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItem.hostname_created'
        db.add_column(u'lab_clinic_reference_referencerangelistitem', 'hostname_created',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItem.hostname_modified'
        db.add_column(u'lab_clinic_reference_referencerangelistitem', 'hostname_modified',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItemAudit.created'
        db.add_column(u'lab_clinic_reference_referencerangelistitem_audit', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItemAudit.modified'
        db.add_column(u'lab_clinic_reference_referencerangelistitem_audit', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItemAudit.user_created'
        db.add_column(u'lab_clinic_reference_referencerangelistitem_audit', 'user_created',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItemAudit.user_modified'
        db.add_column(u'lab_clinic_reference_referencerangelistitem_audit', 'user_modified',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItemAudit.hostname_created'
        db.add_column(u'lab_clinic_reference_referencerangelistitem_audit', 'hostname_created',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'ReferenceRangeListItemAudit.hostname_modified'
        db.add_column(u'lab_clinic_reference_referencerangelistitem_audit', 'hostname_modified',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'GradingListItem.created'
        db.add_column(u'lab_clinic_reference_gradinglistitem', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'GradingListItem.modified'
        db.add_column(u'lab_clinic_reference_gradinglistitem', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'GradingListItem.user_created'
        db.add_column(u'lab_clinic_reference_gradinglistitem', 'user_created',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'GradingListItem.user_modified'
        db.add_column(u'lab_clinic_reference_gradinglistitem', 'user_modified',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'GradingListItem.hostname_created'
        db.add_column(u'lab_clinic_reference_gradinglistitem', 'hostname_created',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)

        # Adding field 'GradingListItem.hostname_modified'
        db.add_column(u'lab_clinic_reference_gradinglistitem', 'hostname_modified',
                      self.gf('django.db.models.fields.CharField')(default='silverapple', max_length=50, db_index=True, blank=True),
                      keep_default=False)


    def backwards(self, orm):
        # Deleting field 'GradingListItemAudit.created'
        db.delete_column(u'lab_clinic_reference_gradinglistitem_audit', 'created')

        # Deleting field 'GradingListItemAudit.modified'
        db.delete_column(u'lab_clinic_reference_gradinglistitem_audit', 'modified')

        # Deleting field 'GradingListItemAudit.user_created'
        db.delete_column(u'lab_clinic_reference_gradinglistitem_audit', 'user_created')

        # Deleting field 'GradingListItemAudit.user_modified'
        db.delete_column(u'lab_clinic_reference_gradinglistitem_audit', 'user_modified')

        # Deleting field 'GradingListItemAudit.hostname_created'
        db.delete_column(u'lab_clinic_reference_gradinglistitem_audit', 'hostname_created')

        # Deleting field 'GradingListItemAudit.hostname_modified'
        db.delete_column(u'lab_clinic_reference_gradinglistitem_audit', 'hostname_modified')

        # Deleting field 'ReferenceRangeList.created'
        db.delete_column(u'lab_clinic_reference_referencerangelist', 'created')

        # Deleting field 'ReferenceRangeList.modified'
        db.delete_column(u'lab_clinic_reference_referencerangelist', 'modified')

        # Deleting field 'ReferenceRangeList.user_created'
        db.delete_column(u'lab_clinic_reference_referencerangelist', 'user_created')

        # Deleting field 'ReferenceRangeList.user_modified'
        db.delete_column(u'lab_clinic_reference_referencerangelist', 'user_modified')

        # Deleting field 'ReferenceRangeList.hostname_created'
        db.delete_column(u'lab_clinic_reference_referencerangelist', 'hostname_created')

        # Deleting field 'ReferenceRangeList.hostname_modified'
        db.delete_column(u'lab_clinic_reference_referencerangelist', 'hostname_modified')

        # Deleting field 'GradingList.created'
        db.delete_column(u'lab_clinic_reference_gradinglist', 'created')

        # Deleting field 'GradingList.modified'
        db.delete_column(u'lab_clinic_reference_gradinglist', 'modified')

        # Deleting field 'GradingList.user_created'
        db.delete_column(u'lab_clinic_reference_gradinglist', 'user_created')

        # Deleting field 'GradingList.user_modified'
        db.delete_column(u'lab_clinic_reference_gradinglist', 'user_modified')

        # Deleting field 'GradingList.hostname_created'
        db.delete_column(u'lab_clinic_reference_gradinglist', 'hostname_created')

        # Deleting field 'GradingList.hostname_modified'
        db.delete_column(u'lab_clinic_reference_gradinglist', 'hostname_modified')

        # Deleting field 'ReferenceRangeListItem.created'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem', 'created')

        # Deleting field 'ReferenceRangeListItem.modified'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem', 'modified')

        # Deleting field 'ReferenceRangeListItem.user_created'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem', 'user_created')

        # Deleting field 'ReferenceRangeListItem.user_modified'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem', 'user_modified')

        # Deleting field 'ReferenceRangeListItem.hostname_created'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem', 'hostname_created')

        # Deleting field 'ReferenceRangeListItem.hostname_modified'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem', 'hostname_modified')

        # Deleting field 'ReferenceRangeListItemAudit.created'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem_audit', 'created')

        # Deleting field 'ReferenceRangeListItemAudit.modified'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem_audit', 'modified')

        # Deleting field 'ReferenceRangeListItemAudit.user_created'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem_audit', 'user_created')

        # Deleting field 'ReferenceRangeListItemAudit.user_modified'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem_audit', 'user_modified')

        # Deleting field 'ReferenceRangeListItemAudit.hostname_created'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem_audit', 'hostname_created')

        # Deleting field 'ReferenceRangeListItemAudit.hostname_modified'
        db.delete_column(u'lab_clinic_reference_referencerangelistitem_audit', 'hostname_modified')

        # Deleting field 'GradingListItem.created'
        db.delete_column(u'lab_clinic_reference_gradinglistitem', 'created')

        # Deleting field 'GradingListItem.modified'
        db.delete_column(u'lab_clinic_reference_gradinglistitem', 'modified')

        # Deleting field 'GradingListItem.user_created'
        db.delete_column(u'lab_clinic_reference_gradinglistitem', 'user_created')

        # Deleting field 'GradingListItem.user_modified'
        db.delete_column(u'lab_clinic_reference_gradinglistitem', 'user_modified')

        # Deleting field 'GradingListItem.hostname_created'
        db.delete_column(u'lab_clinic_reference_gradinglistitem', 'hostname_created')

        # Deleting field 'GradingListItem.hostname_modified'
        db.delete_column(u'lab_clinic_reference_gradinglistitem', 'hostname_modified')


    models = {
        'lab_clinic_api.testcode': {
            'Meta': {'ordering': "['edc_name']", 'object_name': 'TestCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_decimal_places': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'edc_code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'edc_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': "'50'", 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_absolute': ('django.db.models.fields.CharField', [], {'default': "'absolute'", 'max_length': "'15'"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'test_code_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.TestCodeGroup']", 'null': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_clinic_api.testcodegroup': {
            'Meta': {'ordering': "['code']", 'object_name': 'TestCodeGroup'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_clinic_reference.gradinglist': {
            'Meta': {'ordering': "['name']", 'object_name': 'GradingList'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_clinic_reference.gradinglistitem': {
            'Meta': {'ordering': "['test_code', 'age_low', 'age_low_unit']", 'object_name': 'GradingListItem'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'age_high': ('django.db.models.fields.IntegerField', [], {'default': '99999', 'null': 'True', 'blank': 'True'}),
            'age_high_quantifier': ('django.db.models.fields.CharField', [], {'default': "'<='", 'max_length': '10', 'blank': 'True'}),
            'age_high_unit': ('django.db.models.fields.CharField', [], {'default': "'Y'", 'max_length': '10', 'blank': 'True'}),
            'age_low': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'age_low_quantifier': ('django.db.models.fields.CharField', [], {'default': "'>='", 'max_length': '10', 'blank': 'True'}),
            'age_low_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dummy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fasting': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '10'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'grade': ('django.db.models.fields.IntegerField', [], {}),
            'grading_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_reference.GradingList']"}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'panic_value_high': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'panic_value_low': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'scale': ('django.db.models.fields.CharField', [], {'default': "'increasing'", 'max_length': '25'}),
            'serum': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '10'}),
            'test_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.TestCode']"}),
            'use_lln': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_uln': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'value_high': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'value_high_calc': ('django.db.models.fields.CharField', [], {'default': "'ABSOLUTE'", 'max_length': '10'}),
            'value_high_quantifier': ('django.db.models.fields.CharField', [], {'default': "'<='", 'max_length': '10'}),
            'value_low': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'value_low_calc': ('django.db.models.fields.CharField', [], {'default': "'ABSOLUTE'", 'max_length': '10'}),
            'value_low_quantifier': ('django.db.models.fields.CharField', [], {'default': "'>='", 'max_length': '10'}),
            'value_unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'lab_clinic_reference.gradinglistitemaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'GradingListItemAudit', 'db_table': "u'lab_clinic_reference_gradinglistitem_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'age_high': ('django.db.models.fields.IntegerField', [], {'default': '99999', 'null': 'True', 'blank': 'True'}),
            'age_high_quantifier': ('django.db.models.fields.CharField', [], {'default': "'<='", 'max_length': '10', 'blank': 'True'}),
            'age_high_unit': ('django.db.models.fields.CharField', [], {'default': "'Y'", 'max_length': '10', 'blank': 'True'}),
            'age_low': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'age_low_quantifier': ('django.db.models.fields.CharField', [], {'default': "'>='", 'max_length': '10', 'blank': 'True'}),
            'age_low_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dummy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'fasting': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '10'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'grade': ('django.db.models.fields.IntegerField', [], {}),
            'grading_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_gradinglistitem'", 'to': "orm['lab_clinic_reference.GradingList']"}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'import_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'panic_value_high': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'panic_value_low': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'scale': ('django.db.models.fields.CharField', [], {'default': "'increasing'", 'max_length': '25'}),
            'serum': ('django.db.models.fields.CharField', [], {'default': "'N/A'", 'max_length': '10'}),
            'test_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_gradinglistitem'", 'to': "orm['lab_clinic_api.TestCode']"}),
            'use_lln': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'use_uln': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'value_high': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'value_high_calc': ('django.db.models.fields.CharField', [], {'default': "'ABSOLUTE'", 'max_length': '10'}),
            'value_high_quantifier': ('django.db.models.fields.CharField', [], {'default': "'<='", 'max_length': '10'}),
            'value_low': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'value_low_calc': ('django.db.models.fields.CharField', [], {'default': "'ABSOLUTE'", 'max_length': '10'}),
            'value_low_quantifier': ('django.db.models.fields.CharField', [], {'default': "'>='", 'max_length': '10'}),
            'value_unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'lab_clinic_reference.referencerangelist': {
            'Meta': {'ordering': "['name']", 'object_name': 'ReferenceRangeList'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'description': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_clinic_reference.referencerangelistitem': {
            'Meta': {'ordering': "['test_code', 'age_low', 'age_low_unit']", 'object_name': 'ReferenceRangeListItem'},
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'age_high': ('django.db.models.fields.IntegerField', [], {'default': '99999', 'null': 'True', 'blank': 'True'}),
            'age_high_quantifier': ('django.db.models.fields.CharField', [], {'default': "'<='", 'max_length': '10', 'blank': 'True'}),
            'age_high_unit': ('django.db.models.fields.CharField', [], {'default': "'Y'", 'max_length': '10', 'blank': 'True'}),
            'age_low': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'age_low_quantifier': ('django.db.models.fields.CharField', [], {'default': "'>='", 'max_length': '10', 'blank': 'True'}),
            'age_low_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dummy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'panic_value_high': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'panic_value_low': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'reference_range_list': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_reference.ReferenceRangeList']"}),
            'scale': ('django.db.models.fields.CharField', [], {'default': "'increasing'", 'max_length': '25'}),
            'test_code': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.TestCode']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'value_high': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'value_high_quantifier': ('django.db.models.fields.CharField', [], {'default': "'<='", 'max_length': '10'}),
            'value_low': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'value_low_quantifier': ('django.db.models.fields.CharField', [], {'default': "'>='", 'max_length': '10'}),
            'value_unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        },
        'lab_clinic_reference.referencerangelistitemaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ReferenceRangeListItemAudit', 'db_table': "u'lab_clinic_reference_referencerangelistitem_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'age_high': ('django.db.models.fields.IntegerField', [], {'default': '99999', 'null': 'True', 'blank': 'True'}),
            'age_high_quantifier': ('django.db.models.fields.CharField', [], {'default': "'<='", 'max_length': '10', 'blank': 'True'}),
            'age_high_unit': ('django.db.models.fields.CharField', [], {'default': "'Y'", 'max_length': '10', 'blank': 'True'}),
            'age_low': ('django.db.models.fields.IntegerField', [], {'default': '0', 'null': 'True', 'blank': 'True'}),
            'age_low_quantifier': ('django.db.models.fields.CharField', [], {'default': "'>='", 'max_length': '10', 'blank': 'True'}),
            'age_low_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10', 'blank': 'True'}),
            'code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dummy': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'default': "'ANY'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'silverapple'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'import_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'panic_value_high': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'panic_value_low': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'reference_range_list': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_referencerangelistitem'", 'to': "orm['lab_clinic_reference.ReferenceRangeList']"}),
            'scale': ('django.db.models.fields.CharField', [], {'default': "'increasing'", 'max_length': '25'}),
            'test_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_referencerangelistitem'", 'to': "orm['lab_clinic_api.TestCode']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'value_high': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'value_high_quantifier': ('django.db.models.fields.CharField', [], {'default': "'<='", 'max_length': '10'}),
            'value_low': ('django.db.models.fields.DecimalField', [], {'null': 'True', 'max_digits': '12', 'decimal_places': '4', 'blank': 'True'}),
            'value_low_quantifier': ('django.db.models.fields.CharField', [], {'default': "'>='", 'max_length': '10'}),
            'value_unit': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'})
        }
    }

    complete_apps = ['lab_clinic_reference']