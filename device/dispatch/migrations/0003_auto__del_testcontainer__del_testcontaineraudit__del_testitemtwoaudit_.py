# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TestContainer'
        db.delete_table(u'dispatch_testcontainer')

        # Deleting model 'TestContainerAudit'
        db.delete_table(u'dispatch_testcontainer_audit')

        # Deleting model 'TestItemTwoAudit'
        db.delete_table(u'dispatch_testitemtwo_audit')

        # Deleting model 'TestItem'
        db.delete_table(u'dispatch_testitem')

        # Removing M2M table for field test_many_to_many on 'TestItem'
        db.delete_table('dispatch_testitem_test_many_to_many')

        # Deleting model 'TestItemThree'
        db.delete_table(u'dispatch_testitemthree')

        # Deleting model 'TestItemAudit'
        db.delete_table(u'dispatch_testitem_audit')

        # Deleting model 'TestItemM2M'
        db.delete_table(u'dispatch_testitemm2m')

        # Removing M2M table for field m2m on 'TestItemM2M'
        db.delete_table('dispatch_testitemm2m_m2m')

        # Deleting model 'TestItemM2MAudit'
        db.delete_table(u'dispatch_testitemm2m_audit')

        # Deleting model 'TestItemTwo'
        db.delete_table(u'dispatch_testitemtwo')

        # Deleting model 'TestList'
        db.delete_table(u'dispatch_testlist')

        # Deleting model 'TestItemThreeAudit'
        db.delete_table(u'dispatch_testitemthree_audit')


    def backwards(self, orm):
        # Adding model 'TestContainer'
        db.create_table(u'dispatch_testcontainer', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('test_container_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, unique=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
        ))
        db.send_create_signal('dispatch', ['TestContainer'])

        # Adding model 'TestContainerAudit'
        db.create_table(u'dispatch_testcontainer_audit', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_container_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal('dispatch', ['TestContainerAudit'])

        # Adding model 'TestItemTwoAudit'
        db.create_table(u'dispatch_testitemtwo_audit', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testitemtwo', to=orm['dispatch.TestItem'])),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal('dispatch', ['TestItemTwoAudit'])

        # Adding model 'TestItem'
        db.create_table(u'dispatch_testitem', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('test_container', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dispatch.TestContainer'])),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, unique=True)),
        ))
        db.send_create_signal('dispatch', ['TestItem'])

        # Adding M2M table for field test_many_to_many on 'TestItem'
        db.create_table(u'dispatch_testitem_test_many_to_many', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('testitem', models.ForeignKey(orm['dispatch.testitem'], null=False)),
            ('testm2m', models.ForeignKey(orm['bhp_base_model.testm2m'], null=False))
        ))
        db.create_unique(u'dispatch_testitem_test_many_to_many', ['testitem_id', 'testm2m_id'])

        # Adding model 'TestItemThree'
        db.create_table(u'dispatch_testitemthree', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('test_item_two', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dispatch.TestItemTwo'])),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, unique=True)),
        ))
        db.send_create_signal('dispatch', ['TestItemThree'])

        # Adding model 'TestItemAudit'
        db.create_table(u'dispatch_testitem_audit', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('test_container', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testitem', to=orm['dispatch.TestContainer'])),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal('dispatch', ['TestItemAudit'])

        # Adding model 'TestItemM2M'
        db.create_table(u'dispatch_testitemm2m', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item_three', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dispatch.TestItemThree'])),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, unique=True)),
        ))
        db.send_create_signal('dispatch', ['TestItemM2M'])

        # Adding M2M table for field m2m on 'TestItemM2M'
        db.create_table(u'dispatch_testitemm2m_m2m', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('testitemm2m', models.ForeignKey(orm['dispatch.testitemm2m'], null=False)),
            ('testlist', models.ForeignKey(orm['dispatch.testlist'], null=False))
        ))
        db.create_unique(u'dispatch_testitemm2m_m2m', ['testitemm2m_id', 'testlist_id'])

        # Adding model 'TestItemM2MAudit'
        db.create_table(u'dispatch_testitemm2m_audit', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item_three', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testitemm2m', to=orm['dispatch.TestItemThree'])),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal('dispatch', ['TestItemM2MAudit'])

        # Adding model 'TestItemTwo'
        db.create_table(u'dispatch_testitemtwo', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dispatch.TestItem'])),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, unique=True)),
        ))
        db.send_create_signal('dispatch', ['TestItemTwo'])

        # Adding model 'TestList'
        db.create_table(u'dispatch_testlist', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
            ('short_name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250, null=True, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(unique=True, max_length=250, null=True, db_index=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
        ))
        db.send_create_signal('dispatch', ['TestList'])

        # Adding model 'TestItemThreeAudit'
        db.create_table(u'dispatch_testitemthree_audit', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('test_item_two', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testitemthree', to=orm['dispatch.TestItemTwo'])),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, blank=True, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('_audit_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
        ))
        db.send_create_signal('dispatch', ['TestItemThreeAudit'])


    models = {
        'dispatch.dispatchcontainerregister': {
            'Meta': {'unique_together': "(('container_app_label', 'container_model_name', 'container_pk'),)", 'object_name': 'DispatchContainerRegister', 'db_table': "'bhp_dispatch_dispatchcontainerregister'"},
            'container_app_label': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'container_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'container_identifier_attrname': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'container_model_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'container_pk': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dispatch_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 30, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'dispatch_items': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'dispatched_using': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_dispatched': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sync.Producer']"}),
            'return_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'dispatch.dispatchitemregister': {
            'Meta': {'unique_together': "(('dispatch_container_register', 'item_pk', 'item_identifier', 'is_dispatched'),)", 'object_name': 'DispatchItemRegister', 'db_table': "'bhp_dispatch_dispatchitemregister'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dispatch_container_register': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dispatch.DispatchContainerRegister']"}),
            'dispatch_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 30, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'dispatch_host': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'dispatch_using': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_dispatched': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'item_app_label': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '40'}),
            'item_identifier_attrname': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'item_model_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'item_pk': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sync.Producer']"}),
            'registered_subjects': ('django.db.models.fields.TextField', [], {'null': 'True', 'blank': 'True'}),
            'return_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'dispatch.preparehistory': {
            'Meta': {'object_name': 'PrepareHistory', 'db_table': "'bhp_dispatch_preparehistory'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'destination': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'prepare_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 30, 0, 0)'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sync.Producer']"}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'sync.producer': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('settings_key', 'is_active'),)", 'object_name': 'Producer', 'db_table': "'bhp_sync_producer'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'json_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'json_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'settings_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'sync_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'sync_status': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '250', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['dispatch']