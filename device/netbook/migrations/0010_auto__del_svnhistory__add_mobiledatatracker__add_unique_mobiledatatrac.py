# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'SvnHistory'
        db.delete_table(u'netbook_svnhistory')

        # Adding model 'MobileDataTracker'
        db.create_table('bhp_netbook_mobiledatatracker', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('app_label', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('model_name', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('identifier', self.gf('django.db.models.fields.CharField')(max_length=36)),
            ('track_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('track_status', self.gf('django.db.models.fields.CharField')(max_length=15)),
        ))
        db.send_create_signal('netbook', ['MobileDataTracker'])

        # Adding unique constraint on 'MobileDataTracker', fields ['app_label', 'model_name', 'identifier']
        db.create_unique('bhp_netbook_mobiledatatracker', ['app_label', 'model_name', 'identifier'])

        # Adding index on 'NetbookUser', fields ['hostname_modified']
        db.create_index('bhp_netbook_netbookuser', ['hostname_modified'])

        # Adding index on 'NetbookUser', fields ['user_modified']
        db.create_index('bhp_netbook_netbookuser', ['user_modified'])

        # Adding index on 'NetbookUser', fields ['hostname_created']
        db.create_index('bhp_netbook_netbookuser', ['hostname_created'])

        # Adding index on 'NetbookUser', fields ['user_created']
        db.create_index('bhp_netbook_netbookuser', ['user_created'])

        # Adding index on 'Netbook', fields ['hostname_created']
        db.create_index('bhp_netbook_netbook', ['hostname_created'])

        # Adding index on 'Netbook', fields ['user_modified']
        db.create_index('bhp_netbook_netbook', ['user_modified'])

        # Adding index on 'Netbook', fields ['hostname_modified']
        db.create_index('bhp_netbook_netbook', ['hostname_modified'])

        # Adding index on 'Netbook', fields ['user_created']
        db.create_index('bhp_netbook_netbook', ['user_created'])


    def backwards(self, orm):
        # Removing index on 'Netbook', fields ['user_created']
        db.delete_index('bhp_netbook_netbook', ['user_created'])

        # Removing index on 'Netbook', fields ['hostname_modified']
        db.delete_index('bhp_netbook_netbook', ['hostname_modified'])

        # Removing index on 'Netbook', fields ['user_modified']
        db.delete_index('bhp_netbook_netbook', ['user_modified'])

        # Removing index on 'Netbook', fields ['hostname_created']
        db.delete_index('bhp_netbook_netbook', ['hostname_created'])

        # Removing index on 'NetbookUser', fields ['user_created']
        db.delete_index('bhp_netbook_netbookuser', ['user_created'])

        # Removing index on 'NetbookUser', fields ['hostname_created']
        db.delete_index('bhp_netbook_netbookuser', ['hostname_created'])

        # Removing index on 'NetbookUser', fields ['user_modified']
        db.delete_index('bhp_netbook_netbookuser', ['user_modified'])

        # Removing index on 'NetbookUser', fields ['hostname_modified']
        db.delete_index('bhp_netbook_netbookuser', ['hostname_modified'])

        # Removing unique constraint on 'MobileDataTracker', fields ['app_label', 'model_name', 'identifier']
        db.delete_unique('bhp_netbook_mobiledatatracker', ['app_label', 'model_name', 'identifier'])

        # Adding model 'SvnHistory'
        db.create_table(u'netbook_svnhistory', (
            ('last_revision_date', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('last_revision_number', self.gf('django.db.models.fields.IntegerField')(null=True)),
            ('repo', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('netbook', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['netbook.Netbook'])),
            ('id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
        ))
        db.send_create_signal('netbook', ['SvnHistory'])

        # Deleting model 'MobileDataTracker'
        db.delete_table('bhp_netbook_mobiledatatracker')


    models = {
        u'auth.group': {
            'Meta': {'object_name': 'Group'},
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '80'}),
            'permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'})
        },
        u'auth.permission': {
            'Meta': {'ordering': "(u'content_type__app_label', u'content_type__model', u'codename')", 'unique_together': "((u'content_type', u'codename'),)", 'object_name': 'Permission'},
            'codename': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']"}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        u'auth.user': {
            'Meta': {'object_name': 'User'},
            'date_joined': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'email': ('django.db.models.fields.EmailField', [], {'max_length': '75', 'blank': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'groups': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Group']", 'symmetrical': 'False', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'is_staff': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_superuser': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_login': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '30', 'blank': 'True'}),
            'password': ('django.db.models.fields.CharField', [], {'max_length': '128'}),
            'user_permissions': ('django.db.models.fields.related.ManyToManyField', [], {'to': u"orm['auth.Permission']", 'symmetrical': 'False', 'blank': 'True'}),
            'username': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '30'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'netbook.mobiledatatracker': {
            'Meta': {'unique_together': "(['app_label', 'model_name', 'identifier'],)", 'object_name': 'MobileDataTracker', 'db_table': "'bhp_netbook_mobiledatatracker'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'identifier': ('django.db.models.fields.CharField', [], {'max_length': '36'}),
            'model_name': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'track_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'track_status': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'netbook.netbook': {
            'Meta': {'ordering': "['name']", 'object_name': 'Netbook', 'db_table': "'bhp_netbook_netbook'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_purchased': ('django.db.models.fields.DateField', [], {}),
            'db_name': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'ip_address': ('django.db.models.fields.IPAddressField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_alive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'last_seen': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'make': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '10'}),
            'serial_number': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'netbook.netbookuser': {
            'Meta': {'ordering': "['netbook']", 'unique_together': "(['netbook', 'user'],)", 'object_name': 'NetbookUser', 'db_table': "'bhp_netbook_netbookuser'"},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'end_date': ('django.db.models.fields.DateField', [], {'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'netbook': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['netbook.Netbook']"}),
            'start_date': ('django.db.models.fields.DateField', [], {}),
            'user': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['auth.User']", 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        }
    }

    complete_apps = ['netbook']