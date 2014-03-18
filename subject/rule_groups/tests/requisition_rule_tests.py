from django.test import TestCase

from edc.entry_meta_data.models import RequisitionMetaData
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.lab.lab_profile.exceptions import AlreadyRegistered as AlreadyRegisteredLabProfile
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.visit_schedule.models import VisitDefinition
from edc.testing.classes import TestLabProfile
from edc.testing.classes import TestVisitSchedule, TestAppConfiguration
from edc.testing.models import TestVisit, TestRequisition, TestScheduledModel1, TestConsentWithMixin
from edc.testing.tests.factories import TestConsentWithMixinFactory, TestScheduledModel1Factory, TestVisitFactory
from edc.core.bhp_variables.models import StudySite

from ..classes import RuleGroup, BaseRule, RequisitionRule, Logic


class RequisitionRuleTests(TestCase):

    app_label = 'testing'
    consent_catalogue_name = 'v1'

    def setUp(self):

        try:
            site_lab_profiles.register(TestLabProfile())
        except AlreadyRegisteredLabProfile:
            pass
        TestAppConfiguration()
        site_lab_tracker.autodiscover()
        TestVisitSchedule().build()

        # a test rule group where the source model is RegisteredSubject
        # the rules in this rule group will be only evaluated when the visit instance
        # is created or saved. Note source_fk is None.
        class TestRuleGroupRs(RuleGroup):
            test_rule = RequisitionRule(
                logic=Logic(
                    predicate=(('gender', 'equals', 'M')),
                    consequence='not_required',
                    alternative='new'),
                target_model=['testrequisition'])

            class Meta:
                app_label = 'testing'
                source_fk = None
                source_model = RegisteredSubject
        site_rule_groups.register(TestRuleGroupRs)

        # a test rule group where the source model is a scheduled model.
        # a scheduled model has a FK to the visit instance (source_fk).
        # the rules in this rule group will be evaluated when the source instance
        # is created or saved.
        class TestRuleGroupSched(RuleGroup):
            test_rule = RequisitionRule(
                logic=Logic(
                    predicate=(('f1', 'equals', 'No')),
                    consequence='not_required',
                    alternative='new'),
                target_model=['testrequisition'])

            class Meta:
                app_label = 'testing'
                source_fk = (TestVisit, 'test_visit')
                source_model = TestScheduledModel1
        site_rule_groups.register(TestRuleGroupSched)

        # a test rule group where the source model is a consent or membership model.
        # these models have a FK to registered subject (source_fk).
        # the rules in this rule group will only evaluated when the visit instance
        # is created or saved.
        class TestRuleGroupConsent(RuleGroup):
            test_rule = RequisitionRule(
                logic=Logic(
                    predicate=(('may_store_samples', 'equals', 'No')),
                    consequence='not_required',
                    alternative='new'),
                target_model=['testrequisition'])

            class Meta:
                app_label = 'testing'
                source_fk = (RegisteredSubject, 'registered_subject')
                source_model = TestConsentWithMixin
        site_rule_groups.register(TestRuleGroupConsent)

        self.test_rule_group_rs_cls = TestRuleGroupRs
        self.test_rule_group_sched_cls = TestRuleGroupSched
        self.test_rule_group_consent_cls = TestRuleGroupConsent

        self.test_visit_factory = TestVisitFactory

        self.visit_definition = VisitDefinition.objects.get(code='1000')

        self.test_consent = TestConsentWithMixinFactory(gender='M', study_site=StudySite.objects.all()[0], may_store_samples='No')

        self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.test_consent.subject_identifier)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject)

    def test_target_is_requisition1(self):
        class BadRule(RuleGroup):
            test_rule = RequisitionRule(
                logic=Logic(
                    predicate=(('may_store_samples', 'equals', 'No')),
                    consequence='not_required',
                    alternative='new'),
                target_model=['testscheduledmodel1'],
                target_requisition_panel_name=['microtube'])

            class Meta:
                app_label = 'testing'
                source_fk = (RegisteredSubject, 'registered_subject')
                source_model = TestConsentWithMixin
        self.assertRaisesRegexp(TypeError, 'target model', BadRule)

    def test_target_is_requisition2(self):
        class GoodRule(RuleGroup):
            test_rule = RequisitionRule(
                logic=Logic(
                    predicate=(('may_store_samples', 'equals', 'No')),
                    consequence='not_required',
                    alternative='new'),
                target_model=['testrequisition'],
                target_requisition_panel_name=['microtube'])

            class Meta:
                app_label = 'testing'
                source_fk = (RegisteredSubject, 'registered_subject')
                source_model = TestConsentWithMixin
        self.assertTrue(GoodRule().target_models, [TestRequisition])


    def test_rule_updates_meta_data_with_rs(self):
        """Assert updates meta data if source is RegisteredSubject."""
        rg = self.test_rule_group_rs_cls()
        self.assertEquals(self.registered_subject.gender, 'M')
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NOT_REQUIRED', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)

    def test_rule_updates_meta_data_on_update_with_rs(self):
        """Assert updates meta data when the source model is updated."""
        rg = self.test_rule_group_rs_cls()
        self.assertEquals(self.registered_subject.gender, 'M')
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NOT_REQUIRED', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)
        self.registered_subject.gender = 'F'
        self.registered_subject.save()
        self.test_visit = TestVisit.objects.get(appointment=self.appointment)
        self.test_visit.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)

    def test_rule_updates_meta_data_with_consent(self):
        """Assert updates meta data if source is RegisteredSubject and override fields knocked out."""
        rg = self.test_rule_group_consent_cls()
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NOT_REQUIRED', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)

    def test_rule_updates_meta_data_on_update_with_consent(self):
        """Assert updates meta data when the source model is updated."""
        rg = self.test_rule_group_consent_cls()
        self.assertEquals(self.test_consent.may_store_samples, 'No')
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NOT_REQUIRED', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)
        self.test_consent.may_store_samples = 'Yes'
        self.test_consent.save()
        self.test_visit = TestVisit.objects.get(appointment=self.appointment)
        self.test_visit.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)

    def test_rule_updates_meta_data(self):
        """Assert updates meta data when source model is created, if criteria met."""
        rg = self.test_rule_group_sched_cls()
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)

    def test_rule_updates_meta_data2(self):
        """Assert does not update meta data when source model is created, if criteria is not met."""
        rg = self.test_rule_group_sched_cls()
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)
        # set f1=No which is the rule for not required.
        test_scheduled_model1 = TestScheduledModel1Factory(test_visit=self.test_visit, f1='No')
        # meta data for target, testscheduledmodel2, should be updated as not required
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NOT_REQUIRED', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)
        test_scheduled_model1.f1 = 'Yes'
        test_scheduled_model1.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)

    def test_rule_updates_meta_data_on_update(self):
        """Assert updates meta data when the source model is updated."""
        rg = self.test_rule_group_sched_cls()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)
        test_scheduled_model1 = TestScheduledModel1Factory(test_visit=self.test_visit, f1='No')
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NOT_REQUIRED', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)
        test_scheduled_model1.f1 = 'Yes'
        test_scheduled_model1.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, entry__model_name__in=rg.test_rule.target_model_names).count(), 1)
