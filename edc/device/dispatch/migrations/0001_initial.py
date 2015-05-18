# -*- coding: utf-8 -*-
from south.utils import datetime_utils as datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'DispatchContainerRegister'
        db.create_table('bhp_dispatch_dispatchcontainerregister', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('producer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sync.Producer'])),
            ('is_dispatched', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('dispatch_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 17, 0, 0), null=True, blank=True)),
            ('return_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('container_app_label', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('container_model_name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('container_identifier_attrname', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('container_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('container_pk', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dispatched_using', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('dispatch_items', self.gf('django.db.models.fields.TextField')(max_length=500)),
        ))
        db.send_create_signal('dispatch', ['DispatchContainerRegister'])

        # Adding unique constraint on 'DispatchContainerRegister', fields ['container_app_label', 'container_model_name', 'container_pk']
        db.create_unique('bhp_dispatch_dispatchcontainerregister', ['container_app_label', 'container_model_name', 'container_pk'])

        # Adding model 'DispatchItemRegister'
        db.create_table('bhp_dispatch_dispatchitemregister', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('producer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sync.Producer'])),
            ('is_dispatched', self.gf('django.db.models.fields.BooleanField')(default=True)),
            ('dispatch_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 17, 0, 0), null=True, blank=True)),
            ('return_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('dispatch_container_register', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['dispatch.DispatchContainerRegister'])),
            ('item_app_label', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('item_model_name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('item_identifier_attrname', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('item_identifier', self.gf('django.db.models.fields.CharField')(max_length=40)),
            ('item_pk', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('dispatch_host', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('dispatch_using', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('registered_subjects', self.gf('django.db.models.fields.TextField')(null=True, blank=True)),
        ))
        db.send_create_signal('dispatch', ['DispatchItemRegister'])

        # Adding unique constraint on 'DispatchItemRegister', fields ['dispatch_container_register', 'item_pk', 'item_identifier', 'is_dispatched']
        db.create_unique('bhp_dispatch_dispatchitemregister', ['dispatch_container_register_id', 'item_pk', 'item_identifier', 'is_dispatched'])

        # Adding index on 'DispatchItemRegister', fields ['item_app_label', 'item_model_name', 'item_pk', 'is_dispatched']
        db.create_index('bhp_dispatch_dispatchitemregister', ['item_app_label', 'item_model_name', 'item_pk', 'is_dispatched'])

        # Adding model 'PrepareHistory'
        db.create_table('bhp_dispatch_preparehistory', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True)),
            ('source', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('destination', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('producer', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['sync.Producer'])),
            ('prepare_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2014, 11, 17, 0, 0))),
        ))
        db.send_create_signal('dispatch', ['PrepareHistory'])


    def backwards(self, orm):
        # Removing index on 'DispatchItemRegister', fields ['item_app_label', 'item_model_name', 'item_pk', 'is_dispatched']
        db.delete_index('bhp_dispatch_dispatchitemregister', ['item_app_label', 'item_model_name', 'item_pk', 'is_dispatched'])

        # Removing unique constraint on 'DispatchItemRegister', fields ['dispatch_container_register', 'item_pk', 'item_identifier', 'is_dispatched']
        db.delete_unique('bhp_dispatch_dispatchitemregister', ['dispatch_container_register_id', 'item_pk', 'item_identifier', 'is_dispatched'])

        # Removing unique constraint on 'DispatchContainerRegister', fields ['container_app_label', 'container_model_name', 'container_pk']
        db.delete_unique('bhp_dispatch_dispatchcontainerregister', ['container_app_label', 'container_model_name', 'container_pk'])

        # Deleting model 'DispatchContainerRegister'
        db.delete_table('bhp_dispatch_dispatchcontainerregister')

        # Deleting model 'DispatchItemRegister'
        db.delete_table('bhp_dispatch_dispatchitemregister')

        # Deleting model 'PrepareHistory'
        db.delete_table('bhp_dispatch_preparehistory')


    models = {
        'dispatch.dispatchcontainerregister': {
            'Meta': {'unique_together': "(('container_app_label', 'container_model_name', 'container_pk'),)", 'object_name': 'DispatchContainerRegister', 'db_table': "'bhp_dispatch_dispatchcontainerregister'"},
            'container_app_label': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'container_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'container_identifier_attrname': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'container_model_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'container_pk': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dispatch_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 17, 0, 0)', 'null': 'True', 'blank': 'True'}),
            'dispatch_items': ('django.db.models.fields.TextField', [], {'max_length': '500'}),
            'dispatched_using': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_dispatched': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sync.Producer']"}),
            'return_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'dispatch.dispatchitemregister': {
            'Meta': {'unique_together': "(('dispatch_container_register', 'item_pk', 'item_identifier', 'is_dispatched'),)", 'object_name': 'DispatchItemRegister', 'db_table': "'bhp_dispatch_dispatchitemregister'", 'index_together': "[['item_app_label', 'item_model_name', 'item_pk', 'is_dispatched']]"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dispatch_container_register': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['dispatch.DispatchContainerRegister']"}),
            'dispatch_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 17, 0, 0)', 'null': 'True', 'blank': 'True'}),
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
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
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
            'prepare_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2014, 11, 17, 0, 0)'}),
            'producer': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['sync.Producer']"}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'source': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'sync.producer': {
            'Meta': {'ordering': "['name']", 'unique_together': "(('settings_key', 'is_active'),)", 'object_name': 'Producer', 'db_table': "'bhp_sync_producer'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'db_password': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'db_index': 'True'}),
            'db_user': ('django.db.models.fields.CharField', [], {'default': "'root'", 'max_length': '78L', 'null': 'True', 'db_index': 'True'}),
            'db_user_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'db_index': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'json_limit': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'json_total_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'port': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'producer_ip': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'db_index': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'settings_key': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50'}),
            'sync_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'sync_status': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '250', 'null': 'True'}),
            'url': ('django.db.models.fields.CharField', [], {'max_length': '64'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['dispatch']