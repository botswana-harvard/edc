# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding model 'TestBaseOffStudyAudit'
        db.create_table(u'testing_testbaseoffstudy_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('offstudy_date', self.gf('django.db.models.fields.DateField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('has_scheduled_data', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=10)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testbaseoffstudy', to=orm['registration.RegisteredSubject'])),
        ))
        db.send_create_signal('testing', ['TestBaseOffStudyAudit'])

        # Adding model 'TestBaseOffStudy'
        db.create_table(u'testing_testbaseoffstudy', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.RegisteredSubject'], unique=True)),
            ('offstudy_date', self.gf('django.db.models.fields.DateField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('has_scheduled_data', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=10)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('testing', ['TestBaseOffStudy'])

        # Adding model 'TestRegistration'
        db.create_table(u'testing_testregistration', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.RegisteredSubject'], unique=True)),
            ('registration_datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('testing', ['TestRegistration'])

        # Adding model 'TestConsentHistory'
        db.create_table(u'testing_testconsenthistory', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['registration.RegisteredSubject'])),
            ('consent_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('consent_pk', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('consent_app_label', self.gf('django.db.models.fields.CharField')(max_length=50)),
            ('consent_model_name', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('testing', ['TestConsentHistory'])

        # Adding model 'TestConsent'
        db.create_table(u'testing_testconsent', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier_as_pk', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True)),
            ('is_dob_estimated', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('subject_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('study_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_variables.StudySite'])),
            ('consent_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('guardian_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_store_samples', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('is_incarcerated', self.gf('django.db.models.fields.CharField')(default='-', max_length=3)),
            ('is_literate', self.gf('django.db.models.fields.CharField')(default='-', max_length=3)),
            ('witness_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('consent_version_on_entry', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_version_recent', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_reviewed', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('study_questions', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('assessment_score', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('consent_copy', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='not specified', max_length=25)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_verified_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.RegisteredSubject'], unique=True, null=True)),
            ('user_provided_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=78L, unique=True, null=True, blank=True)),
            ('identity_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('confirm_identity', self.gf('django.db.models.fields.CharField')(max_length=78L, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('testing', ['TestConsent'])

        # Adding model 'TestConsentWithMixin'
        db.create_table(u'testing_testconsentwithmixin', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier_as_pk', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True)),
            ('is_dob_estimated', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('subject_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('study_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_variables.StudySite'])),
            ('consent_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('guardian_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_store_samples', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('is_incarcerated', self.gf('django.db.models.fields.CharField')(default='-', max_length=3)),
            ('is_literate', self.gf('django.db.models.fields.CharField')(default='-', max_length=3)),
            ('witness_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('consent_version_on_entry', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_version_recent', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_reviewed', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('study_questions', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('assessment_score', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('consent_copy', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='not specified', max_length=25)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_verified_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.RegisteredSubject'], unique=True, null=True)),
            ('user_provided_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=78L, unique=True, null=True, blank=True)),
            ('identity_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('confirm_identity', self.gf('django.db.models.fields.CharField')(max_length=78L, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('testing', ['TestConsentWithMixin'])

        # Adding model 'TestConsentNoRs'
        db.create_table(u'testing_testconsentnors', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('subject_identifier_as_pk', self.gf('django.db.models.fields.CharField')(max_length=50, null=True, db_index=True)),
            ('first_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('last_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True)),
            ('initials', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('dob', self.gf('django.db.models.fields.DateField')(null=True)),
            ('is_dob_estimated', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('gender', self.gf('django.db.models.fields.CharField')(max_length=1, null=True)),
            ('subject_type', self.gf('django.db.models.fields.CharField')(max_length=25, null=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(db_index=True, max_length=50, blank=True)),
            ('study_site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_variables.StudySite'])),
            ('consent_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('guardian_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_store_samples', self.gf('django.db.models.fields.CharField')(max_length=3)),
            ('is_incarcerated', self.gf('django.db.models.fields.CharField')(default='-', max_length=3)),
            ('is_literate', self.gf('django.db.models.fields.CharField')(default='-', max_length=3)),
            ('witness_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=250, null=True, blank=True)),
            ('consent_version_on_entry', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_version_recent', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('consent_reviewed', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('study_questions', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('assessment_score', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('consent_copy', self.gf('django.db.models.fields.CharField')(max_length=3, null=True, blank=True)),
            ('language', self.gf('django.db.models.fields.CharField')(default='not specified', max_length=25)),
            ('is_verified', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_verified_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True)),
            ('user_provided_subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=35, null=True)),
            ('identity', self.gf('django.db.models.fields.CharField')(max_length=78L, unique=True, null=True, blank=True)),
            ('identity_type', self.gf('django.db.models.fields.CharField')(max_length=15)),
            ('confirm_identity', self.gf('django.db.models.fields.CharField')(max_length=78L, unique=True, null=True, blank=True)),
        ))
        db.send_create_signal('testing', ['TestConsentNoRs'])

        # Adding model 'TestVisit'
        db.create_table(u'testing_testvisit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('appointment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['appointment.Appointment'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason_missed', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('info_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('info_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('testing', ['TestVisit'])

        # Adding model 'TestSubjectVisit'
        db.create_table(u'testing_testsubjectvisit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('appointment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['appointment.Appointment'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason_missed', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('info_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('info_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('testing', ['TestSubjectVisit'])

        # Adding model 'TestSubjectVisitTwo'
        db.create_table(u'testing_testsubjectvisittwo', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('appointment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['appointment.Appointment'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason_missed', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('info_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('info_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('testing', ['TestSubjectVisitTwo'])

        # Adding model 'TestSubjectVisitThree'
        db.create_table(u'testing_testsubjectvisitthree', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('appointment', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['appointment.Appointment'], unique=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('reason_missed', self.gf('django.db.models.fields.CharField')(max_length=35, null=True, blank=True)),
            ('info_source', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('info_source_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=50)),
        ))
        db.send_create_signal('testing', ['TestSubjectVisitThree'])

        # Adding model 'TestScheduledModel'
        db.create_table(u'testing_testscheduledmodel', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('test_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['testing.TestVisit'], unique=True)),
        ))
        db.send_create_signal('testing', ['TestScheduledModel'])

        # Adding model 'TestForeignKey'
        db.create_table(u'testing_testforeignkey', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, db_index=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, db_index=True)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
        ))
        db.send_create_signal('testing', ['TestForeignKey'])

        # Adding model 'TestM2m'
        db.create_table(u'testing_testm2m', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, db_index=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, db_index=True)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
        ))
        db.send_create_signal('testing', ['TestM2m'])

        # Adding model 'TestSubjectUuidModel'
        db.create_table(u'testing_testsubjectuuidmodel', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.RegisteredSubject'], unique=True)),
            ('test_foreign_key', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testing.TestForeignKey'])),
        ))
        db.send_create_signal('testing', ['TestSubjectUuidModel'])

        # Adding M2M table for field test_m2m on 'TestSubjectUuidModel'
        db.create_table(u'testing_testsubjectuuidmodel_test_m2m', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('testsubjectuuidmodel', models.ForeignKey(orm['testing.testsubjectuuidmodel'], null=False)),
            ('testm2m', models.ForeignKey(orm['testing.testm2m'], null=False))
        ))
        db.create_unique(u'testing_testsubjectuuidmodel_test_m2m', ['testsubjectuuidmodel_id', 'testm2m_id'])

        # Adding model 'TestOffStudy'
        db.create_table(u'testing_testoffstudy', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.RegisteredSubject'], unique=True)),
            ('offstudy_date', self.gf('django.db.models.fields.DateField')()),
            ('reason', self.gf('django.db.models.fields.CharField')(max_length=30)),
            ('reason_other', self.gf('django.db.models.fields.CharField')(max_length=35, blank=True)),
            ('has_scheduled_data', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=10)),
            ('comment', self.gf('django.db.models.fields.TextField')(max_length=250, null=True, blank=True)),
        ))
        db.send_create_signal('testing', ['TestOffStudy'])

        # Adding model 'TestModel'
        db.create_table(u'testing_testmodel', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('f1', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('f2', self.gf('django.db.models.fields.CharField')(max_length=10)),
            ('f3', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('f4', self.gf('django.db.models.fields.CharField')(max_length=10, null=True)),
            ('f5', self.gf('django.db.models.fields.CharField')(max_length=10)),
        ))
        db.send_create_signal('testing', ['TestModel'])

        # Adding model 'TestRequisitionAudit'
        db.create_table(u'testing_testrequisition_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('requisition_identifier', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('requisition_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('specimen_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('protocol', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testrequisition', to=orm['bhp_variables.StudySite'])),
            ('clinician_initials', self.gf('django.db.models.fields.CharField')(default='--', max_length=3, null=True, blank=True)),
            ('aliquot_type', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testrequisition', to=orm['lab_clinic_api.AliquotType'])),
            ('panel', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testrequisition', to=orm['lab_clinic_api.Panel'])),
            ('priority', self.gf('django.db.models.fields.CharField')(default='normal', max_length=25)),
            ('is_drawn', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3)),
            ('reason_not_drawn', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('drawn_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('item_type', self.gf('django.db.models.fields.CharField')(default='tube', max_length=25)),
            ('item_count_total', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('estimated_volume', self.gf('django.db.models.fields.DecimalField')(default=5.0, max_digits=7, decimal_places=1)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=25, null=True, blank=True)),
            ('is_receive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_receive_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_packed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_labelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_labelled_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_lis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test_visit', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testrequisition', to=orm['testing.TestVisit'])),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('testing', ['TestRequisitionAudit'])

        # Adding model 'TestRequisition'
        db.create_table(u'testing_testrequisition', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('requisition_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=25)),
            ('requisition_datetime', self.gf('django.db.models.fields.DateTimeField')()),
            ('specimen_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, unique=True, null=True, blank=True)),
            ('protocol', self.gf('django.db.models.fields.CharField')(max_length=10, null=True, blank=True)),
            ('site', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['bhp_variables.StudySite'])),
            ('clinician_initials', self.gf('django.db.models.fields.CharField')(default='--', max_length=3, null=True, blank=True)),
            ('aliquot_type', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_clinic_api.AliquotType'])),
            ('panel', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['lab_clinic_api.Panel'])),
            ('priority', self.gf('django.db.models.fields.CharField')(default='normal', max_length=25)),
            ('is_drawn', self.gf('django.db.models.fields.CharField')(default='Yes', max_length=3)),
            ('reason_not_drawn', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('drawn_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('item_type', self.gf('django.db.models.fields.CharField')(default='tube', max_length=25)),
            ('item_count_total', self.gf('django.db.models.fields.IntegerField')(default=1)),
            ('estimated_volume', self.gf('django.db.models.fields.DecimalField')(default=5.0, max_digits=7, decimal_places=1)),
            ('comments', self.gf('django.db.models.fields.TextField')(max_length=25, null=True, blank=True)),
            ('is_receive', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_receive_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_packed', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_labelled', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('is_labelled_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, blank=True)),
            ('is_lis', self.gf('django.db.models.fields.BooleanField')(default=False)),
            ('test_visit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testing.TestVisit'])),
        ))
        db.send_create_signal('testing', ['TestRequisition'])

        # Adding M2M table for field test_code on 'TestRequisition'
        db.create_table(u'testing_testrequisition_test_code', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('testrequisition', models.ForeignKey(orm['testing.testrequisition'], null=False)),
            ('testcode', models.ForeignKey(orm['lab_clinic_api.testcode'], null=False))
        ))
        db.create_unique(u'testing_testrequisition_test_code', ['testrequisition_id', 'testcode_id'])

        # Adding model 'TestSubjectResultModel'
        db.create_table(u'testing_testsubjectresultmodel', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('test_visit', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testing.TestVisit'], null=True)),
            ('subject_identifier', self.gf('django.db.models.fields.CharField')(max_length=25, db_index=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(null=True, db_index=True)),
            ('result', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('result_datetime', self.gf('django.db.models.fields.DateTimeField')()),
        ))
        db.send_create_signal('testing', ['TestSubjectResultModel'])

        # Adding model 'TestSubjectLocator'
        db.create_table(u'testing_testsubjectlocator', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('registered_subject', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['registration.RegisteredSubject'], unique=True, null=True)),
            ('report_datetime', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime(2013, 9, 30, 0, 0))),
            ('date_signed', self.gf('django.db.models.fields.DateField')(default=datetime.datetime(2013, 9, 30, 0, 0))),
            ('mail_address', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('home_visit_permission', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('physical_address', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('may_follow_up', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('subject_cell', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('subject_cell_alt', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('subject_phone', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('subject_phone_alt', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_call_work', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('subject_work_place', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('subject_work_phone', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('may_contact_someone', self.gf('django.db.models.fields.CharField')(max_length=25)),
            ('contact_name', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('contact_rel', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('contact_physical_address', self.gf('django.db.models.fields.CharField')(max_length=500, null=True, blank=True)),
            ('contact_cell', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('contact_phone', self.gf('django.db.models.fields.CharField')(max_length=78L, null=True, blank=True)),
            ('test_visit', self.gf('django.db.models.fields.related.OneToOneField')(to=orm['testing.TestVisit'], unique=True)),
        ))
        db.send_create_signal('testing', ['TestSubjectLocator'])

        # Adding model 'EncryptedTestModelAudit'
        db.create_table(u'testing_encryptedtestmodel_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('char1', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('lastname2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('char2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('text1', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('char3', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('text2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('firstname2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('text3', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
            (u'id', self.gf('django.db.models.fields.IntegerField')(db_index=True)),
        ))
        db.send_create_signal('testing', ['EncryptedTestModelAudit'])

        # Adding model 'EncryptedTestModel'
        db.create_table(u'testing_encryptedtestmodel', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('firstname', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('lastname', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('char1', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('lastname2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('char2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('text1', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('char3', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('text2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('firstname2', self.gf('django.db.models.fields.CharField')(max_length=78L)),
            ('text3', self.gf('django.db.models.fields.CharField')(max_length=78L)),
        ))
        db.send_create_signal('testing', ['EncryptedTestModel'])

        # Adding model 'TestDspList'
        db.create_table(u'testing_testdsplist', (
            (u'id', self.gf('django.db.models.fields.AutoField')(primary_key=True)),
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, db_index=True)),
            ('short_name', self.gf('django.db.models.fields.CharField')(max_length=250, unique=True, null=True, db_index=True)),
            ('display_index', self.gf('django.db.models.fields.IntegerField')(default=0, db_index=True)),
            ('field_name', self.gf('django.db.models.fields.CharField')(max_length=25, null=True, blank=True)),
            ('version', self.gf('django.db.models.fields.CharField')(default='1.0', max_length=35)),
        ))
        db.send_create_signal('testing', ['TestDspList'])

        # Adding model 'TestDspContainerAudit'
        db.create_table(u'testing_testdspcontainer_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('test_container_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('testing', ['TestDspContainerAudit'])

        # Adding model 'TestDspContainer'
        db.create_table(u'testing_testdspcontainer', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('test_container_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=35)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('testing', ['TestDspContainer'])

        # Adding model 'TestDspItemAudit'
        db.create_table(u'testing_testdspitem_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('test_container', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testdspitem', to=orm['testing.TestDspContainer'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('testing', ['TestDspItemAudit'])

        # Adding model 'TestDspItem'
        db.create_table(u'testing_testdspitem', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=35)),
            ('test_container', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testing.TestDspContainer'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('testing', ['TestDspItem'])

        # Adding M2M table for field test_m2m on 'TestDspItem'
        db.create_table(u'testing_testdspitem_test_m2m', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('testdspitem', models.ForeignKey(orm['testing.testdspitem'], null=False)),
            ('testm2m', models.ForeignKey(orm['testing.testm2m'], null=False))
        ))
        db.create_unique(u'testing_testdspitem_test_m2m', ['testdspitem_id', 'testm2m_id'])

        # Adding model 'TestDspItemTwoAudit'
        db.create_table(u'testing_testdspitemtwo_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('test_item', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testdspitemtwo', to=orm['testing.TestDspItem'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('testing', ['TestDspItemTwoAudit'])

        # Adding model 'TestDspItemTwo'
        db.create_table(u'testing_testdspitemtwo', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=35)),
            ('test_item', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testing.TestDspItem'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('testing', ['TestDspItemTwo'])

        # Adding model 'TestDspItemThreeAudit'
        db.create_table(u'testing_testdspitemthree_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('test_item_two', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testdspitemthree', to=orm['testing.TestDspItemTwo'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('testing', ['TestDspItemThreeAudit'])

        # Adding model 'TestDspItemThree'
        db.create_table(u'testing_testdspitemthree', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=35)),
            ('test_item_two', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testing.TestDspItemTwo'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('testing', ['TestDspItemThree'])

        # Adding model 'TestDspItemM2MAudit'
        db.create_table(u'testing_testdspitemm2m_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('test_item_three', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testdspitemm2m', to=orm['testing.TestDspItemThree'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('testing', ['TestDspItemM2MAudit'])

        # Adding model 'TestDspItemM2M'
        db.create_table(u'testing_testdspitemm2m', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=35)),
            ('test_item_three', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testing.TestDspItemThree'])),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('testing', ['TestDspItemM2M'])

        # Adding M2M table for field m2m on 'TestDspItemM2M'
        db.create_table(u'testing_testdspitemm2m_m2m', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('testdspitemm2m', models.ForeignKey(orm['testing.testdspitemm2m'], null=False)),
            ('testdsplist', models.ForeignKey(orm['testing.testdsplist'], null=False))
        ))
        db.create_unique(u'testing_testdspitemm2m_m2m', ['testdspitemm2m_id', 'testdsplist_id'])

        # Adding model 'TestDspItemBypassAudit'
        db.create_table(u'testing_testdspitembypass_audit', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, blank=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('test_container', self.gf('django.db.models.fields.related.ForeignKey')(related_name='_audit_testdspitembypass', to=orm['testing.TestDspContainer'])),
            ('f1', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('f2', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('f3', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('f4', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
            ('_audit_id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('_audit_timestamp', self.gf('django.db.models.fields.DateTimeField')(auto_now_add=True, db_index=True, blank=True)),
            ('_audit_change_type', self.gf('django.db.models.fields.CharField')(max_length=1)),
        ))
        db.send_create_signal('testing', ['TestDspItemBypassAudit'])

        # Adding model 'TestDspItemBypass'
        db.create_table(u'testing_testdspitembypass', (
            ('created', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('modified', self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True)),
            ('user_created', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('user_modified', self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True)),
            ('hostname_created', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('hostname_modified', self.gf('django.db.models.fields.CharField')(default='mac.local', max_length=50, db_index=True, blank=True)),
            ('id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True)),
            ('test_item_identifier', self.gf('django.db.models.fields.CharField')(unique=True, max_length=35)),
            ('test_container', self.gf('django.db.models.fields.related.ForeignKey')(to=orm['testing.TestDspContainer'])),
            ('f1', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('f2', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('f3', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('f4', self.gf('django.db.models.fields.CharField')(max_length=35)),
            ('comment', self.gf('django.db.models.fields.CharField')(max_length=50, null=True)),
        ))
        db.send_create_signal('testing', ['TestDspItemBypass'])

        # Adding M2M table for field test_m2m on 'TestDspItemBypass'
        db.create_table(u'testing_testdspitembypass_test_m2m', (
            ('id', models.AutoField(verbose_name='ID', primary_key=True, auto_created=True)),
            ('testdspitembypass', models.ForeignKey(orm['testing.testdspitembypass'], null=False)),
            ('testm2m', models.ForeignKey(orm['testing.testm2m'], null=False))
        ))
        db.create_unique(u'testing_testdspitembypass_test_m2m', ['testdspitembypass_id', 'testm2m_id'])


    def backwards(self, orm):
        # Deleting model 'TestBaseOffStudyAudit'
        db.delete_table(u'testing_testbaseoffstudy_audit')

        # Deleting model 'TestBaseOffStudy'
        db.delete_table(u'testing_testbaseoffstudy')

        # Deleting model 'TestRegistration'
        db.delete_table(u'testing_testregistration')

        # Deleting model 'TestConsentHistory'
        db.delete_table(u'testing_testconsenthistory')

        # Deleting model 'TestConsent'
        db.delete_table(u'testing_testconsent')

        # Deleting model 'TestConsentWithMixin'
        db.delete_table(u'testing_testconsentwithmixin')

        # Deleting model 'TestConsentNoRs'
        db.delete_table(u'testing_testconsentnors')

        # Deleting model 'TestVisit'
        db.delete_table(u'testing_testvisit')

        # Deleting model 'TestSubjectVisit'
        db.delete_table(u'testing_testsubjectvisit')

        # Deleting model 'TestSubjectVisitTwo'
        db.delete_table(u'testing_testsubjectvisittwo')

        # Deleting model 'TestSubjectVisitThree'
        db.delete_table(u'testing_testsubjectvisitthree')

        # Deleting model 'TestScheduledModel'
        db.delete_table(u'testing_testscheduledmodel')

        # Deleting model 'TestForeignKey'
        db.delete_table(u'testing_testforeignkey')

        # Deleting model 'TestM2m'
        db.delete_table(u'testing_testm2m')

        # Deleting model 'TestSubjectUuidModel'
        db.delete_table(u'testing_testsubjectuuidmodel')

        # Removing M2M table for field test_m2m on 'TestSubjectUuidModel'
        db.delete_table('testing_testsubjectuuidmodel_test_m2m')

        # Deleting model 'TestOffStudy'
        db.delete_table(u'testing_testoffstudy')

        # Deleting model 'TestModel'
        db.delete_table(u'testing_testmodel')

        # Deleting model 'TestRequisitionAudit'
        db.delete_table(u'testing_testrequisition_audit')

        # Deleting model 'TestRequisition'
        db.delete_table(u'testing_testrequisition')

        # Removing M2M table for field test_code on 'TestRequisition'
        db.delete_table('testing_testrequisition_test_code')

        # Deleting model 'TestSubjectResultModel'
        db.delete_table(u'testing_testsubjectresultmodel')

        # Deleting model 'TestSubjectLocator'
        db.delete_table(u'testing_testsubjectlocator')

        # Deleting model 'EncryptedTestModelAudit'
        db.delete_table(u'testing_encryptedtestmodel_audit')

        # Deleting model 'EncryptedTestModel'
        db.delete_table(u'testing_encryptedtestmodel')

        # Deleting model 'TestDspList'
        db.delete_table(u'testing_testdsplist')

        # Deleting model 'TestDspContainerAudit'
        db.delete_table(u'testing_testdspcontainer_audit')

        # Deleting model 'TestDspContainer'
        db.delete_table(u'testing_testdspcontainer')

        # Deleting model 'TestDspItemAudit'
        db.delete_table(u'testing_testdspitem_audit')

        # Deleting model 'TestDspItem'
        db.delete_table(u'testing_testdspitem')

        # Removing M2M table for field test_m2m on 'TestDspItem'
        db.delete_table('testing_testdspitem_test_m2m')

        # Deleting model 'TestDspItemTwoAudit'
        db.delete_table(u'testing_testdspitemtwo_audit')

        # Deleting model 'TestDspItemTwo'
        db.delete_table(u'testing_testdspitemtwo')

        # Deleting model 'TestDspItemThreeAudit'
        db.delete_table(u'testing_testdspitemthree_audit')

        # Deleting model 'TestDspItemThree'
        db.delete_table(u'testing_testdspitemthree')

        # Deleting model 'TestDspItemM2MAudit'
        db.delete_table(u'testing_testdspitemm2m_audit')

        # Deleting model 'TestDspItemM2M'
        db.delete_table(u'testing_testdspitemm2m')

        # Removing M2M table for field m2m on 'TestDspItemM2M'
        db.delete_table('testing_testdspitemm2m_m2m')

        # Deleting model 'TestDspItemBypassAudit'
        db.delete_table(u'testing_testdspitembypass_audit')

        # Deleting model 'TestDspItemBypass'
        db.delete_table(u'testing_testdspitembypass')

        # Removing M2M table for field test_m2m on 'TestDspItemBypass'
        db.delete_table('testing_testdspitembypass_test_m2m')


    models = {
        'appointment.appointment': {
            'Meta': {'ordering': "['registered_subject', 'appt_datetime']", 'unique_together': "(('registered_subject', 'visit_definition', 'visit_instance'),)", 'object_name': 'Appointment', 'db_table': "'bhp_appointment_appointment'"},
            'appt_close_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'appt_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'appt_reason': ('django.db.models.fields.CharField', [], {'max_length': '25', 'blank': 'True'}),
            'appt_status': ('django.db.models.fields.CharField', [], {'default': "'new'", 'max_length': '25', 'db_index': 'True'}),
            'appt_type': ('django.db.models.fields.CharField', [], {'default': "'clinic'", 'max_length': '20'}),
            'best_appt_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'contact_count': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'contact_tel': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dashboard_type': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_confirmed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['registration.RegisteredSubject']"}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']", 'null': 'True'}),
            'timepoint_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visit_definition': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['visit_schedule.VisitDefinition']"}),
            'visit_instance': ('django.db.models.fields.CharField', [], {'default': "'0'", 'max_length': '1', 'null': 'True', 'db_index': 'True', 'blank': 'True'})
        },
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
        'bhp_variables.studysite': {
            'Meta': {'ordering': "['site_code']", 'unique_together': "[('site_code', 'site_name')]", 'object_name': 'StudySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'site_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'site_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        u'contenttypes.contenttype': {
            'Meta': {'ordering': "('name',)", 'unique_together': "(('app_label', 'model'),)", 'object_name': 'ContentType', 'db_table': "'django_content_type'"},
            'app_label': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'model': ('django.db.models.fields.CharField', [], {'max_length': '100'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '100'})
        },
        'lab_clinic_api.aliquottype': {
            'Meta': {'ordering': "['name']", 'object_name': 'AliquotType'},
            'alpha_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_clinic_api.panel': {
            'Meta': {'object_name': 'Panel'},
            'aliquot_type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lab_clinic_api.AliquotType']", 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'edc_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'panel_type': ('django.db.models.fields.CharField', [], {'default': "'TEST'", 'max_length': '15'}),
            'test_code': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lab_clinic_api.TestCode']", 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'lab_clinic_api.testcode': {
            'Meta': {'ordering': "['edc_name']", 'object_name': 'TestCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_decimal_places': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'edc_code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'edc_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': "'50'", 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
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
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'registration.registeredsubject': {
            'Meta': {'ordering': "['subject_identifier']", 'unique_together': "(('first_name', 'dob', 'initials'),)", 'object_name': 'RegisteredSubject', 'db_table': "'bhp_registration_registeredsubject'"},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'randomization_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_identifier': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'relative_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'screening_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']", 'null': 'True', 'blank': 'True'}),
            'subject_consent_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'survival_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.encryptedtestmodel': {
            'Meta': {'object_name': 'EncryptedTestModel'},
            'char1': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'char2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'char3': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'firstname2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'lastname2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'text1': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'text2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'text3': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.encryptedtestmodelaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'EncryptedTestModelAudit', 'db_table': "u'testing_encryptedtestmodel_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'char1': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'char2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'char3': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'firstname': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'firstname2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.IntegerField', [], {'db_index': 'True'}),
            'lastname': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'lastname2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'text1': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'text2': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'text3': ('django.db.models.fields.CharField', [], {'max_length': '78L'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testbaseoffstudy': {
            'Meta': {'object_name': 'TestBaseOffStudy'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_scheduled_data': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'offstudy_date': ('django.db.models.fields.DateField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegisteredSubject']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testbaseoffstudyaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestBaseOffStudyAudit', 'db_table': "u'testing_testbaseoffstudy_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_scheduled_data': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'offstudy_date': ('django.db.models.fields.DateField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testbaseoffstudy'", 'to': "orm['registration.RegisteredSubject']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testconsent': {
            'Meta': {'object_name': 'TestConsent'},
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'not specified'", 'max_length': '25'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegisteredSubject']", 'unique': 'True', 'null': 'True'}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_provided_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'testing.testconsenthistory': {
            'Meta': {'object_name': 'TestConsentHistory'},
            'consent_app_label': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_model_name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'consent_pk': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.RegisteredSubject']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testconsentnors': {
            'Meta': {'object_name': 'TestConsentNoRs'},
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'not specified'", 'max_length': '25'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_provided_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'testing.testconsentwithmixin': {
            'Meta': {'object_name': 'TestConsentWithMixin'},
            'assessment_score': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'confirm_identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'consent_copy': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'consent_reviewed': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'consent_version_on_entry': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'consent_version_recent': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'guardian_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'is_incarcerated': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_literate': ('django.db.models.fields.CharField', [], {'default': "'-'", 'max_length': '3'}),
            'is_verified': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_verified_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'language': ('django.db.models.fields.CharField', [], {'default': "'not specified'", 'max_length': '25'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegisteredSubject']", 'unique': 'True', 'null': 'True'}),
            'study_questions': ('django.db.models.fields.CharField', [], {'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']"}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_provided_subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True'}),
            'witness_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'})
        },
        'testing.testdspcontainer': {
            'Meta': {'object_name': 'TestDspContainer'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_container_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdspcontaineraudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestDspContainerAudit', 'db_table': "u'testing_testdspcontainer_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_container_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdspitem': {
            'Meta': {'object_name': 'TestDspItem'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testing.TestDspContainer']"}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'test_m2m': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['testing.TestM2m']", 'symmetrical': 'False'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdspitemaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestDspItemAudit', 'db_table': "u'testing_testdspitem_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testdspitem'", 'to': "orm['testing.TestDspContainer']"}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdspitembypass': {
            'Meta': {'object_name': 'TestDspItemBypass'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'f1': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'f2': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'f3': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'f4': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_container': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testing.TestDspContainer']"}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'test_m2m': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['testing.TestM2m']", 'symmetrical': 'False'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdspitembypassaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestDspItemBypassAudit', 'db_table': "u'testing_testdspitembypass_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'f1': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'f2': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'f3': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'f4': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_container': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testdspitembypass'", 'to': "orm['testing.TestDspContainer']"}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdspitemm2m': {
            'Meta': {'object_name': 'TestDspItemM2M'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'm2m': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['testing.TestDspList']", 'symmetrical': 'False'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'test_item_three': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testing.TestDspItemThree']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdspitemm2maudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestDspItemM2MAudit', 'db_table': "u'testing_testdspitemm2m_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'test_item_three': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testdspitemm2m'", 'to': "orm['testing.TestDspItemThree']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdspitemthree': {
            'Meta': {'object_name': 'TestDspItemThree'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'test_item_two': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testing.TestDspItemTwo']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdspitemthreeaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestDspItemThreeAudit', 'db_table': "u'testing_testdspitemthree_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'test_item_two': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testdspitemthree'", 'to': "orm['testing.TestDspItemTwo']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdspitemtwo': {
            'Meta': {'object_name': 'TestDspItemTwo'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_item': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testing.TestDspItem']"}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdspitemtwoaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestDspItemTwoAudit', 'db_table': "u'testing_testdspitemtwo_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_item': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testdspitemtwo'", 'to': "orm['testing.TestDspItem']"}),
            'test_item_identifier': ('django.db.models.fields.CharField', [], {'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testdsplist': {
            'Meta': {'object_name': 'TestDspList'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'testing.testforeignkey': {
            'Meta': {'object_name': 'TestForeignKey'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'testing.testm2m': {
            'Meta': {'object_name': 'TestM2m'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'testing.testmodel': {
            'Meta': {'object_name': 'TestModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'f1': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'f2': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'f3': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'f4': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True'}),
            'f5': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testoffstudy': {
            'Meta': {'object_name': 'TestOffStudy'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'has_scheduled_data': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '10'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'offstudy_date': ('django.db.models.fields.DateField', [], {}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '30'}),
            'reason_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegisteredSubject']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testregistration': {
            'Meta': {'object_name': 'TestRegistration'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegisteredSubject']", 'unique': 'True'}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testrequisition': {
            'Meta': {'object_name': 'TestRequisition'},
            'aliquot_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.AliquotType']"}),
            'clinician_initials': ('django.db.models.fields.CharField', [], {'default': "'--'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'drawn_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'estimated_volume': ('django.db.models.fields.DecimalField', [], {'default': '5.0', 'max_digits': '7', 'decimal_places': '1'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'is_drawn': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3'}),
            'is_labelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_labelled_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_lis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_packed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_receive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_receive_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'item_count_total': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'item_type': ('django.db.models.fields.CharField', [], {'default': "'tube'", 'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'panel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.Panel']"}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '25'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'reason_not_drawn': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'requisition_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'requisition_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']"}),
            'specimen_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'unique': 'True', 'null': 'True', 'blank': 'True'}),
            'test_code': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lab_clinic_api.TestCode']", 'null': 'True', 'blank': 'True'}),
            'test_visit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testing.TestVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testrequisitionaudit': {
            'Meta': {'ordering': "['-_audit_timestamp']", 'object_name': 'TestRequisitionAudit', 'db_table': "u'testing_testrequisition_audit'"},
            '_audit_change_type': ('django.db.models.fields.CharField', [], {'max_length': '1'}),
            '_audit_id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            '_audit_timestamp': ('django.db.models.fields.DateTimeField', [], {'auto_now_add': 'True', 'db_index': 'True', 'blank': 'True'}),
            'aliquot_type': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testrequisition'", 'to': "orm['lab_clinic_api.AliquotType']"}),
            'clinician_initials': ('django.db.models.fields.CharField', [], {'default': "'--'", 'max_length': '3', 'null': 'True', 'blank': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'drawn_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'estimated_volume': ('django.db.models.fields.DecimalField', [], {'default': '5.0', 'max_digits': '7', 'decimal_places': '1'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'blank': 'True'}),
            'is_drawn': ('django.db.models.fields.CharField', [], {'default': "'Yes'", 'max_length': '3'}),
            'is_labelled': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_labelled_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'is_lis': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_packed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_receive': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'is_receive_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'item_count_total': ('django.db.models.fields.IntegerField', [], {'default': '1'}),
            'item_type': ('django.db.models.fields.CharField', [], {'default': "'tube'", 'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'panel': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testrequisition'", 'to': "orm['lab_clinic_api.Panel']"}),
            'priority': ('django.db.models.fields.CharField', [], {'default': "'normal'", 'max_length': '25'}),
            'protocol': ('django.db.models.fields.CharField', [], {'max_length': '10', 'null': 'True', 'blank': 'True'}),
            'reason_not_drawn': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'requisition_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'requisition_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'site': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testrequisition'", 'to': "orm['bhp_variables.StudySite']"}),
            'specimen_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'test_visit': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'_audit_testrequisition'", 'to': "orm['testing.TestVisit']"}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testscheduledmodel': {
            'Meta': {'object_name': 'TestScheduledModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'test_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['testing.TestVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testsubjectlocator': {
            'Meta': {'object_name': 'TestSubjectLocator'},
            'contact_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'contact_physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'contact_rel': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'date_signed': ('django.db.models.fields.DateField', [], {'default': 'datetime.datetime(2013, 9, 30, 0, 0)'}),
            'home_visit_permission': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'mail_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'may_call_work': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_contact_someone': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'may_follow_up': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'physical_address': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegisteredSubject']", 'unique': 'True', 'null': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2013, 9, 30, 0, 0)'}),
            'subject_cell': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_cell_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_phone_alt': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_work_phone': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'subject_work_place': ('django.db.models.fields.CharField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'test_visit': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['testing.TestVisit']", 'unique': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testsubjectresultmodel': {
            'Meta': {'object_name': 'TestSubjectResultModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'db_index': 'True'}),
            'result': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'result_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'test_visit': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testing.TestVisit']", 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testsubjectuuidmodel': {
            'Meta': {'object_name': 'TestSubjectUuidModel'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '10'}),
            'registered_subject': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['registration.RegisteredSubject']", 'unique': 'True'}),
            'test_foreign_key': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['testing.TestForeignKey']"}),
            'test_m2m': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['testing.TestM2m']", 'symmetrical': 'False'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testsubjectvisit': {
            'Meta': {'object_name': 'TestSubjectVisit'},
            'appointment': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['appointment.Appointment']", 'unique': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'info_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'info_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_missed': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testsubjectvisitthree': {
            'Meta': {'object_name': 'TestSubjectVisitThree'},
            'appointment': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['appointment.Appointment']", 'unique': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'info_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'info_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_missed': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testsubjectvisittwo': {
            'Meta': {'object_name': 'TestSubjectVisitTwo'},
            'appointment': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['appointment.Appointment']", 'unique': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'info_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'info_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_missed': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'testing.testvisit': {
            'Meta': {'object_name': 'TestVisit'},
            'appointment': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['appointment.Appointment']", 'unique': 'True'}),
            'comments': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'info_source': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'info_source_other': ('django.db.models.fields.CharField', [], {'max_length': '35', 'blank': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'reason': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'reason_missed': ('django.db.models.fields.CharField', [], {'max_length': '35', 'null': 'True', 'blank': 'True'}),
            'report_datetime': ('django.db.models.fields.DateTimeField', [], {}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'visit_schedule.membershipform': {
            'Meta': {'object_name': 'MembershipForm', 'db_table': "'bhp_visit_membershipform'"},
            'category': ('django.db.models.fields.CharField', [], {'default': "'subject'", 'max_length': '25', 'null': 'True'}),
            'content_type_map': ('django.db.models.fields.related.OneToOneField', [], {'related_name': "'+'", 'unique': 'True', 'to': "orm['bhp_content_type_map.ContentTypeMap']"}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visible': ('django.db.models.fields.BooleanField', [], {'default': 'True'})
        },
        'visit_schedule.schedulegroup': {
            'Meta': {'ordering': "['group_name']", 'object_name': 'ScheduleGroup', 'db_table': "'bhp_visit_schedulegroup'"},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'group_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'grouping_key': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'membership_form': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['visit_schedule.MembershipForm']"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'})
        },
        'visit_schedule.visitdefinition': {
            'Meta': {'ordering': "['code', 'time_point']", 'object_name': 'VisitDefinition', 'db_table': "'bhp_visit_visitdefinition'"},
            'base_interval': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'base_interval_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '6', 'db_index': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'grouping': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'default': "'mac.local'", 'max_length': '50', 'db_index': 'True', 'blank': 'True'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'instruction': ('django.db.models.fields.TextField', [], {'max_length': '255', 'blank': 'True'}),
            'lower_window': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'lower_window_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'schedule_group': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['visit_schedule.ScheduleGroup']", 'null': 'True', 'blank': 'True'}),
            'time_point': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '35', 'db_index': 'True'}),
            'upper_window': ('django.db.models.fields.IntegerField', [], {'default': '0'}),
            'upper_window_unit': ('django.db.models.fields.CharField', [], {'default': "'D'", 'max_length': '10'}),
            'user_created': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'default': "''", 'max_length': '250', 'db_index': 'True'}),
            'visit_tracking_content_type_map': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_content_type_map.ContentTypeMap']", 'null': 'True'})
        }
    }

    complete_apps = ['testing']