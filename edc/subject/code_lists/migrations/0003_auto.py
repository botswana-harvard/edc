# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'SsxCode', fields ['hostname_created']
        db.create_index('bhp_code_lists_ssxcode', ['hostname_created'])

        # Adding index on 'SsxCode', fields ['user_modified']
        db.create_index('bhp_code_lists_ssxcode', ['user_modified'])

        # Adding index on 'SsxCode', fields ['hostname_modified']
        db.create_index('bhp_code_lists_ssxcode', ['hostname_modified'])

        # Adding index on 'SsxCode', fields ['user_created']
        db.create_index('bhp_code_lists_ssxcode', ['user_created'])

        # Adding index on 'BodySiteCode', fields ['hostname_created']
        db.create_index('bhp_code_lists_bodysitecode', ['hostname_created'])

        # Adding index on 'BodySiteCode', fields ['user_modified']
        db.create_index('bhp_code_lists_bodysitecode', ['user_modified'])

        # Adding index on 'BodySiteCode', fields ['hostname_modified']
        db.create_index('bhp_code_lists_bodysitecode', ['hostname_modified'])

        # Adding index on 'BodySiteCode', fields ['user_created']
        db.create_index('bhp_code_lists_bodysitecode', ['user_created'])

        # Adding index on 'WcsDxPed', fields ['hostname_created']
        db.create_index('bhp_code_lists_wcsdxped', ['hostname_created'])

        # Adding index on 'WcsDxPed', fields ['user_modified']
        db.create_index('bhp_code_lists_wcsdxped', ['user_modified'])

        # Adding index on 'WcsDxPed', fields ['hostname_modified']
        db.create_index('bhp_code_lists_wcsdxped', ['hostname_modified'])

        # Adding index on 'WcsDxPed', fields ['user_created']
        db.create_index('bhp_code_lists_wcsdxped', ['user_created'])

        # Adding index on 'DxCode', fields ['hostname_created']
        db.create_index('bhp_code_lists_dxcode', ['hostname_created'])

        # Adding index on 'DxCode', fields ['user_modified']
        db.create_index('bhp_code_lists_dxcode', ['user_modified'])

        # Adding index on 'DxCode', fields ['hostname_modified']
        db.create_index('bhp_code_lists_dxcode', ['hostname_modified'])

        # Adding index on 'DxCode', fields ['user_created']
        db.create_index('bhp_code_lists_dxcode', ['user_created'])

        # Adding index on 'MedicationCode', fields ['hostname_created']
        db.create_index('bhp_code_lists_medicationcode', ['hostname_created'])

        # Adding index on 'MedicationCode', fields ['user_modified']
        db.create_index('bhp_code_lists_medicationcode', ['user_modified'])

        # Adding index on 'MedicationCode', fields ['hostname_modified']
        db.create_index('bhp_code_lists_medicationcode', ['hostname_modified'])

        # Adding index on 'MedicationCode', fields ['user_created']
        db.create_index('bhp_code_lists_medicationcode', ['user_created'])

        # Adding index on 'ArvCode', fields ['hostname_created']
        db.create_index('bhp_code_lists_arvcode', ['hostname_created'])

        # Adding index on 'ArvCode', fields ['user_modified']
        db.create_index('bhp_code_lists_arvcode', ['user_modified'])

        # Adding index on 'ArvCode', fields ['hostname_modified']
        db.create_index('bhp_code_lists_arvcode', ['hostname_modified'])

        # Adding index on 'ArvCode', fields ['user_created']
        db.create_index('bhp_code_lists_arvcode', ['user_created'])

        # Adding index on 'OrganismCode', fields ['hostname_created']
        db.create_index('bhp_code_lists_organismcode', ['hostname_created'])

        # Adding index on 'OrganismCode', fields ['user_modified']
        db.create_index('bhp_code_lists_organismcode', ['user_modified'])

        # Adding index on 'OrganismCode', fields ['hostname_modified']
        db.create_index('bhp_code_lists_organismcode', ['hostname_modified'])

        # Adding index on 'OrganismCode', fields ['user_created']
        db.create_index('bhp_code_lists_organismcode', ['user_created'])

        # Adding index on 'WcsDxAdult', fields ['hostname_created']
        db.create_index('bhp_code_lists_wcsdxadult', ['hostname_created'])

        # Adding index on 'WcsDxAdult', fields ['user_modified']
        db.create_index('bhp_code_lists_wcsdxadult', ['user_modified'])

        # Adding index on 'WcsDxAdult', fields ['hostname_modified']
        db.create_index('bhp_code_lists_wcsdxadult', ['hostname_modified'])

        # Adding index on 'WcsDxAdult', fields ['user_created']
        db.create_index('bhp_code_lists_wcsdxadult', ['user_created'])

        # Adding index on 'ArvModificationCode', fields ['hostname_created']
        db.create_index('bhp_code_lists_arvmodificationcode', ['hostname_created'])

        # Adding index on 'ArvModificationCode', fields ['user_modified']
        db.create_index('bhp_code_lists_arvmodificationcode', ['user_modified'])

        # Adding index on 'ArvModificationCode', fields ['hostname_modified']
        db.create_index('bhp_code_lists_arvmodificationcode', ['hostname_modified'])

        # Adding index on 'ArvModificationCode', fields ['user_created']
        db.create_index('bhp_code_lists_arvmodificationcode', ['user_created'])

        # Adding index on 'ArvDoseStatus', fields ['hostname_created']
        db.create_index('bhp_code_lists_arvdosestatus', ['hostname_created'])

        # Adding index on 'ArvDoseStatus', fields ['user_modified']
        db.create_index('bhp_code_lists_arvdosestatus', ['user_modified'])

        # Adding index on 'ArvDoseStatus', fields ['hostname_modified']
        db.create_index('bhp_code_lists_arvdosestatus', ['hostname_modified'])

        # Adding index on 'ArvDoseStatus', fields ['user_created']
        db.create_index('bhp_code_lists_arvdosestatus', ['user_created'])


    def backwards(self, orm):
        # Removing index on 'ArvDoseStatus', fields ['user_created']
        db.delete_index('bhp_code_lists_arvdosestatus', ['user_created'])

        # Removing index on 'ArvDoseStatus', fields ['hostname_modified']
        db.delete_index('bhp_code_lists_arvdosestatus', ['hostname_modified'])

        # Removing index on 'ArvDoseStatus', fields ['user_modified']
        db.delete_index('bhp_code_lists_arvdosestatus', ['user_modified'])

        # Removing index on 'ArvDoseStatus', fields ['hostname_created']
        db.delete_index('bhp_code_lists_arvdosestatus', ['hostname_created'])

        # Removing index on 'ArvModificationCode', fields ['user_created']
        db.delete_index('bhp_code_lists_arvmodificationcode', ['user_created'])

        # Removing index on 'ArvModificationCode', fields ['hostname_modified']
        db.delete_index('bhp_code_lists_arvmodificationcode', ['hostname_modified'])

        # Removing index on 'ArvModificationCode', fields ['user_modified']
        db.delete_index('bhp_code_lists_arvmodificationcode', ['user_modified'])

        # Removing index on 'ArvModificationCode', fields ['hostname_created']
        db.delete_index('bhp_code_lists_arvmodificationcode', ['hostname_created'])

        # Removing index on 'WcsDxAdult', fields ['user_created']
        db.delete_index('bhp_code_lists_wcsdxadult', ['user_created'])

        # Removing index on 'WcsDxAdult', fields ['hostname_modified']
        db.delete_index('bhp_code_lists_wcsdxadult', ['hostname_modified'])

        # Removing index on 'WcsDxAdult', fields ['user_modified']
        db.delete_index('bhp_code_lists_wcsdxadult', ['user_modified'])

        # Removing index on 'WcsDxAdult', fields ['hostname_created']
        db.delete_index('bhp_code_lists_wcsdxadult', ['hostname_created'])

        # Removing index on 'OrganismCode', fields ['user_created']
        db.delete_index('bhp_code_lists_organismcode', ['user_created'])

        # Removing index on 'OrganismCode', fields ['hostname_modified']
        db.delete_index('bhp_code_lists_organismcode', ['hostname_modified'])

        # Removing index on 'OrganismCode', fields ['user_modified']
        db.delete_index('bhp_code_lists_organismcode', ['user_modified'])

        # Removing index on 'OrganismCode', fields ['hostname_created']
        db.delete_index('bhp_code_lists_organismcode', ['hostname_created'])

        # Removing index on 'ArvCode', fields ['user_created']
        db.delete_index('bhp_code_lists_arvcode', ['user_created'])

        # Removing index on 'ArvCode', fields ['hostname_modified']
        db.delete_index('bhp_code_lists_arvcode', ['hostname_modified'])

        # Removing index on 'ArvCode', fields ['user_modified']
        db.delete_index('bhp_code_lists_arvcode', ['user_modified'])

        # Removing index on 'ArvCode', fields ['hostname_created']
        db.delete_index('bhp_code_lists_arvcode', ['hostname_created'])

        # Removing index on 'MedicationCode', fields ['user_created']
        db.delete_index('bhp_code_lists_medicationcode', ['user_created'])

        # Removing index on 'MedicationCode', fields ['hostname_modified']
        db.delete_index('bhp_code_lists_medicationcode', ['hostname_modified'])

        # Removing index on 'MedicationCode', fields ['user_modified']
        db.delete_index('bhp_code_lists_medicationcode', ['user_modified'])

        # Removing index on 'MedicationCode', fields ['hostname_created']
        db.delete_index('bhp_code_lists_medicationcode', ['hostname_created'])

        # Removing index on 'DxCode', fields ['user_created']
        db.delete_index('bhp_code_lists_dxcode', ['user_created'])

        # Removing index on 'DxCode', fields ['hostname_modified']
        db.delete_index('bhp_code_lists_dxcode', ['hostname_modified'])

        # Removing index on 'DxCode', fields ['user_modified']
        db.delete_index('bhp_code_lists_dxcode', ['user_modified'])

        # Removing index on 'DxCode', fields ['hostname_created']
        db.delete_index('bhp_code_lists_dxcode', ['hostname_created'])

        # Removing index on 'WcsDxPed', fields ['user_created']
        db.delete_index('bhp_code_lists_wcsdxped', ['user_created'])

        # Removing index on 'WcsDxPed', fields ['hostname_modified']
        db.delete_index('bhp_code_lists_wcsdxped', ['hostname_modified'])

        # Removing index on 'WcsDxPed', fields ['user_modified']
        db.delete_index('bhp_code_lists_wcsdxped', ['user_modified'])

        # Removing index on 'WcsDxPed', fields ['hostname_created']
        db.delete_index('bhp_code_lists_wcsdxped', ['hostname_created'])

        # Removing index on 'BodySiteCode', fields ['user_created']
        db.delete_index('bhp_code_lists_bodysitecode', ['user_created'])

        # Removing index on 'BodySiteCode', fields ['hostname_modified']
        db.delete_index('bhp_code_lists_bodysitecode', ['hostname_modified'])

        # Removing index on 'BodySiteCode', fields ['user_modified']
        db.delete_index('bhp_code_lists_bodysitecode', ['user_modified'])

        # Removing index on 'BodySiteCode', fields ['hostname_created']
        db.delete_index('bhp_code_lists_bodysitecode', ['hostname_created'])

        # Removing index on 'SsxCode', fields ['user_created']
        db.delete_index('bhp_code_lists_ssxcode', ['user_created'])

        # Removing index on 'SsxCode', fields ['hostname_modified']
        db.delete_index('bhp_code_lists_ssxcode', ['hostname_modified'])

        # Removing index on 'SsxCode', fields ['user_modified']
        db.delete_index('bhp_code_lists_ssxcode', ['user_modified'])

        # Removing index on 'SsxCode', fields ['hostname_created']
        db.delete_index('bhp_code_lists_ssxcode', ['hostname_created'])


    models = {
        'code_lists.arvcode': {
            'Meta': {'object_name': 'ArvCode', 'db_table': "'bhp_code_lists_arvcode'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_ref': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'code_lists.arvdosestatus': {
            'Meta': {'object_name': 'ArvDoseStatus', 'db_table': "'bhp_code_lists_arvdosestatus'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_ref': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'code_lists.arvmodificationcode': {
            'Meta': {'object_name': 'ArvModificationCode', 'db_table': "'bhp_code_lists_arvmodificationcode'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_ref': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'code_lists.bodysitecode': {
            'Meta': {'object_name': 'BodySiteCode', 'db_table': "'bhp_code_lists_bodysitecode'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_ref': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'code_lists.dxcode': {
            'Meta': {'object_name': 'DxCode', 'db_table': "'bhp_code_lists_dxcode'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_ref': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'code_lists.medicationcode': {
            'Meta': {'object_name': 'MedicationCode', 'db_table': "'bhp_code_lists_medicationcode'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_ref': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'code_lists.organismcode': {
            'Meta': {'object_name': 'OrganismCode', 'db_table': "'bhp_code_lists_organismcode'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_ref': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'code_lists.ssxcode': {
            'Meta': {'object_name': 'SsxCode', 'db_table': "'bhp_code_lists_ssxcode'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_ref': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'code_lists.wcsdxadult': {
            'Meta': {'object_name': 'WcsDxAdult', 'db_table': "'bhp_code_lists_wcsdxadult'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_ref': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'code_lists.wcsdxped': {
            'Meta': {'object_name': 'WcsDxPed', 'db_table': "'bhp_code_lists_wcsdxped'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'list_ref': ('django.db.models.fields.CharField', [], {'max_length': '100', 'blank': 'True'}),
            'long_name': ('django.db.models.fields.CharField', [], {'max_length': '255', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['code_lists']