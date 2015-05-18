# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding index on 'Appendix40', fields ['hostname_created']
        db.create_index('bhp_actg_reference_appendix40', ['hostname_created'])

        # Adding index on 'Appendix40', fields ['user_modified']
        db.create_index('bhp_actg_reference_appendix40', ['user_modified'])

        # Adding index on 'Appendix40', fields ['hostname_modified']
        db.create_index('bhp_actg_reference_appendix40', ['hostname_modified'])

        # Adding index on 'Appendix40', fields ['user_created']
        db.create_index('bhp_actg_reference_appendix40', ['user_created'])


    def backwards(self, orm):
        # Removing index on 'Appendix40', fields ['user_created']
        db.delete_index('bhp_actg_reference_appendix40', ['user_created'])

        # Removing index on 'Appendix40', fields ['hostname_modified']
        db.delete_index('bhp_actg_reference_appendix40', ['hostname_modified'])

        # Removing index on 'Appendix40', fields ['user_modified']
        db.delete_index('bhp_actg_reference_appendix40', ['user_modified'])

        # Removing index on 'Appendix40', fields ['hostname_created']
        db.delete_index('bhp_actg_reference_appendix40', ['hostname_created'])


    models = {
        'actg.appendix40': {
            'Meta': {'object_name': 'Appendix40', 'db_table': "'bhp_actg_reference_appendix40'"},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'full_description': ('django.db.models.fields.TextField', [], {'max_length': '600'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'short_description': ('django.db.models.fields.CharField', [], {'max_length': '300'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['actg']