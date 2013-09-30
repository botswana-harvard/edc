# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Deleting model 'TestSubjectUuidModel'
        db.delete_table(u'consent_testsubjectuuidmodel')

        # Removing M2M table for field test_many_to_many on 'TestSubjectUuidModel'
        db.delete_table('consent_testsubjectuuidmodel_test_many_to_many')

        # Deleting model 'TestSubjectConsent'
        db.delete_table(u'consent_testsubjectconsent')

        # Deleting model 'TestSubjectConsentNoRS'
        db.delete_table(u'consent_testsubjectconsentnors')

#         # Deleting field 'AttachedModelAudit._audit_subject_identifier'
#         db.delete_column('bhp_consent_attachedmodel_audit', '_audit_subject_identifier')
# 
#         # Deleting field 'ConsentCatalogueAudit._audit_subject_identifier'
#         db.delete_column('bhp_consent_consentcatalogue_audit', '_audit_subject_identifier')


    def backwards(self, orm):
        # Adding model 'TestSubjectUuidModel'
        db.create_table(u'consent_testsubjectuuidmodel', (
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.RegisteredSubject'], unique=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('test_foreign_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_base_model.TestForeignKey'])),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
        ))
        db.send_create_signal('consent', ['TestSubjectUuidModel'])

        # Adding M2M table for field test_many_to_many on 'TestSubjectUuidModel'
        db.create_table(u'consent_testsubjectuuidmodel_test_many_to_many', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('testsubjectuuidmodel', models.ForeignKey(orm['consent.testsubjectuuidmodel'], null=False)),
            ('testm2m', models.ForeignKey(orm['bhp_base_model.testm2m'], null=False))
        ))
        db.create_unique(u'consent_testsubjectuuidmodel_test_many_to_many', ['testsubjectuuidmodel_id', 'testm2m_id'])

        # Adding model 'TestSubjectConsent'
        db.create_table(u'consent_testsubjectconsent', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('confirm_identity', self.gf('django.db.models.fields.CharField')(unique=True, max_length=78L, null=True, blank=True)),
            ('consent_reviewed', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('may_store_samples', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('consent_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('witness_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('assessment_score', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('consent_version_on_entry', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_version_recent', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.RegisteredSubject'], unique=True, null=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50, unique=True, db_index=True)),
            ('is_literate', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3)),
            ('subject_identifier_as_pk', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('consent_copy', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('identity', self.gf('django.db.models.fields.CharField')(unique=True, max_length=78L, null=True, blank=True)),
            ('user_provided_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('study_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_variables.StudySite'])),
            ('identity_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('subject_type', self.gf('django.db.models.fields.CharField')(default='undetermined', max_length=25, null=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('is_verified_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('guardian_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('is_dob_estimated', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('study_questions', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_incarcerated', self.gf('django.db.models.fields.CharField')(default='No', max_length=3)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3, null=True)),
        ))
        db.send_create_signal('consent', ['TestSubjectConsent'])

        # Adding model 'TestSubjectConsentNoRS'
        db.create_table(u'consent_testsubjectconsentnors', (
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('confirm_identity', self.gf('django.db.models.fields.CharField')(unique=True, max_length=78L, null=True, blank=True)),
            ('consent_reviewed', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('may_store_samples', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('consent_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('witness_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('assessment_score', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('consent_version_on_entry', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_version_recent', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(blank=True, max_length=50, unique=True, db_index=True)),
            ('is_literate', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3)),
            ('subject_identifier_as_pk', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True)),
            ('consent_copy', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('identity', self.gf('django.db.models.fields.CharField')(unique=True, max_length=78L, null=True, blank=True)),
            ('user_provided_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('study_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_variables.StudySite'])),
            ('identity_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('subject_type', self.gf('django.db.models.fields.CharField')(default='undetermined', max_length=25, null=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('is_verified_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('guardian_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('is_dob_estimated', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('study_questions', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3, null=True, blank=True)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_incarcerated', self.gf('django.db.models.fields.CharField')(default='No', max_length=3)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, blank=True, db_index=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=3, null=True)),
        ))
        db.send_create_signal('consent', ['TestSubjectConsentNoRS'])

        # Adding field 'AttachedModelAudit._audit_subject_identifier'
        db.add_column('bhp_consent_attachedmodel_audit', '_audit_subject_identifier',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)

        # Adding field 'ConsentCatalogueAudit._audit_subject_identifier'
        db.add_column('bhp_consent_consentcatalogue_audit', '_audit_subject_identifier',
                      self.gf('django.db.models.fields.CharField')(max_length=50, null=True),
                      keep_default=False)


    models = {
        'bhp_content_type_map.contenttypemap': {
            'Meta': {'ordering': "['name']", 'unique_together': "(['app_label', 'model'],)", 'object_name': 'ContentTypeMap'},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'content_type': ('django.db.models.fields.related.ForeignKey', [], {'to': u"orm['contenttypes.ContentType']", 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '50', 'db_index': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'module_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'consent.attachedmodel': {
            'Meta': {'unique_together': "(('consent_catalogue', 'content_type_map'),)", 'object_name': 'AttachedModel', 'db_table': "'bhp_consent_attachedmodel'"},
            'consent_catalogue': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['consent.ConsentCatalogue']"}),
            'content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_content_type_map.ContentTypeMap']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'consent.attachedmodelaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'AttachedModelAudit', 'db_table': "'bhp_consent_attachedmodel_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'consent_catalogue': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_attachedmodel'", 'to': "orm['consent.ConsentCatalogue']"}),
            'content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_attachedmodel'", 'to': "orm['bhp_content_type_map.ContentTypeMap']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'is_active': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'consent.consentcatalogue': {
            'Meta': {'ordering': "['name', 'version']", 'unique_together': "(('name', 'version'),)", 'object_name': 'ConsentCatalogue', 'db_table': "'bhp_consent_consentcatalogue'"},
            'add_for_app': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'consent_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_content_type_map.ContentTypeMap']", 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'list_for_update': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {})
        },
        'consent.consentcatalogueaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'ConsentCatalogueAudit', 'db_table': "'bhp_consent_consentcatalogue_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'add_for_app': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'consent_type': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_consentcatalogue'", 'null': 'True', 'to': "orm['bhp_content_type_map.ContentTypeMap']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'end_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'list_for_update': ('django.db.models.fields.BooleanField', [], {'default': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'start_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.IntegerField', [], {})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        }
    }

    complete_apps = ['consent']