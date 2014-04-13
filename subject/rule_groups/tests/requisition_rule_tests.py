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
from edc.testing.models import TestVisit, TestScheduledModel1, TestConsentWithMixin, TestPanel, TestAliquotType
from edc.testing.tests.factories import TestConsentWithMixinFactory, TestScheduledModel1Factory, TestVisitFactory, TestRequisitionFactory
from edc.core.bhp_variables.models import StudySite
from edc.subject.entry.models import RequisitionPanel
from edc.constants import NOT_REQUIRED, REQUIRED

from ..classes import RuleGroup, RequisitionRule, Logic


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

        class TestRuleGroupConsent(RuleGroup):
            test_rule = RequisitionRule(
                logic=Logic(
                    predicate=(('may_store_samples', 'equals', 'No')),
                    consequence='not_required',
                    alternative='new'),
                target_model=['testrequisition'],
                target_requisition_panels=['research blood draw'])

            class Meta:
                app_label = 'testing'
                source_fk = (RegisteredSubject, 'registered_subject')
                source_model = TestConsentWithMixin
        site_rule_groups.register(TestRuleGroupConsent)

        class TestRuleGroupSched(RuleGroup):
            test_rule = RequisitionRule(
                logic=Logic(
                    predicate=(('f1', 'equals', 'No')),
                    consequence='not_required',
                    alternative='new'),
                target_model=['testrequisition'],
                target_requisition_panels=['microtube', 'viral load'])

            class Meta:
                app_label = 'testing'
                source_fk = (TestVisit, 'test_visit')
                source_model = TestScheduledModel1
        site_rule_groups.register(TestRuleGroupSched)

        self.test_rule_group_sched_cls = TestRuleGroupSched

        self.test_visit_factory = TestVisitFactory

        self.visit_definition = VisitDefinition.objects.get(code='1000')

        self.test_consent = TestConsentWithMixinFactory(gender='M', study_site=StudySite.objects.all()[0], may_store_samples='Yes')

        self.registered_subject = RegisteredSubject.objects.get(subject_identifier=self.test_consent.subject_identifier)
        self.appointment = Appointment.objects.get(registered_subject=self.registered_subject)

#     def test_target_is_requisition1(self):
#         class BadRule(RuleGroup):
#             test_rule = RequisitionRule(
#                 logic=Logic(
#                     predicate=(('may_store_samples', 'equals', 'No')),
#                     consequence='not_required',
#                     alternative='new'),
#                 target_model=['testscheduledmodel1'],
#                 target_requisition_panels=['microtube'])
# 
#             class Meta:
#                 app_label = 'testing'
#                 source_fk = (RegisteredSubject, 'registered_subject')
#                 source_model = TestConsentWithMixin
#         self.assertRaisesRegexp(TypeError, 'target model', BadRule)

    def test_rule(self):
        """Assert sets the target_requisition_panels."""
        test_rule = RequisitionRule(
            logic=Logic(
                predicate=(('may_store_samples', 'equals', 'No')),
                consequence='not_required',
                alternative='new'),
            target_model=['testrequisition'],
            target_requisition_panels=['microtube'])
        self.assertEqual(test_rule.target_requisition_panels, ['microtube'])

    def test_target_is_requisition1(self):
        """Assert sets the target_requisition_panels."""
        self.test_consent.may_store_samples = 'No'
        self.test_consent.save()
        # create the meta data
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        # get the requisition panel (used on lab_entry)
        requisition_panel = RequisitionPanel.objects.get(name__iexact='Research Blood Draw')
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 3)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject, entry_status=NOT_REQUIRED).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel, entry_status=NOT_REQUIRED).count(), 1)

    def test_rule_updates_meta_data2(self):
        """Assert all required if source model instance does not exist."""
        rg = self.test_rule_group_sched_cls()
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject, lab_entry__model_name__in=rg.test_rule.target_model_names).count(), 3)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, lab_entry__model_name__in=rg.test_rule.target_model_names).count(), 3)

    def test_rule_updates_meta_data3(self):
        """Assert updates meta data when the source model is created."""
        rg = self.test_rule_group_sched_cls()
        self.assertEqual(RequisitionMetaData.objects.filter(registered_subject=self.registered_subject).count(), 0)
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, lab_entry__model_name__in=rg.test_rule.target_model_names).count(), 3)
        TestScheduledModel1Factory(test_visit=self.test_visit, f1='No')
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, lab_entry__model_name__in=rg.test_rule.target_model_names).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, registered_subject=self.registered_subject).count(), 2)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject).exclude(lab_entry__requisition_panel__name__in=['Microtube', 'Viral Load']).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, registered_subject=self.registered_subject, lab_entry__requisition_panel__name__in=['Microtube', 'Viral Load']).count(), 2)

    def test_rule_updates_meta_data4(self):
        """Assert updates meta data when the source model is updated."""
        requisition_panels = []
        requisition_panels.append(RequisitionPanel.objects.get(name='Microtube'))
        requisition_panels.append(RequisitionPanel.objects.get(name='Viral Load'))
        self.test_visit = self.test_visit_factory(appointment=self.appointment)
        test_scheduled_model1 = TestScheduledModel1Factory(test_visit=self.test_visit, f1='No')
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, registered_subject=self.registered_subject, lab_entry__requisition_panel__in=requisition_panels).count(), 2)
        test_scheduled_model1.f1 = 'Yes'
        test_scheduled_model1.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, lab_entry__requisition_panel__in=requisition_panels).count(), 2)

    def test_rule_updates_meta_data5(self):
        """Assert updates meta data if target model is KEYED."""
        requisition_panel = RequisitionPanel.objects.get(name='Microtube')
        test_panel = TestPanel.objects.get(name=requisition_panel.name)
        test_aliquot_type = TestAliquotType.objects.get(alpha_code='WB')
        test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject).count(), 3)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
        TestRequisitionFactory(test_visit=test_visit, panel=test_panel, aliquot_type=test_aliquot_type)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED', registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)

    def test_rule_updates_meta_data6(self):
        """Assert updates meta data if target model is KEYED."""
        requisition_panel = RequisitionPanel.objects.get(name='Microtube')
#         test_panel = TestPanel.objects.get(name=requisition_panel.name)
#         test_aliquot_type = TestAliquotType.objects.get(alpha_code='WB')
        test_visit = self.test_visit_factory(appointment=self.appointment)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
        test_scheduled_model1 = TestScheduledModel1Factory(test_visit=test_visit, f1='No')
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
        test_scheduled_model1.f1 = 'Yes'
        test_scheduled_model1.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='NEW', registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)

    def test_rule_updates_meta_data7(self):
        """Assert updates meta data if target model is KEYED, but ignores the rule."""
        requisition_panel = RequisitionPanel.objects.get(name='Microtube')
        test_panel = TestPanel.objects.get(name=requisition_panel.name)
        test_aliquot_type = TestAliquotType.objects.get(alpha_code='WB')
        test_visit = self.test_visit_factory(appointment=self.appointment)
        TestRequisitionFactory(test_visit=test_visit, panel=test_panel, aliquot_type=test_aliquot_type)
        self.assertEqual(RequisitionMetaData.objects.filter(appointment=test_visit.appointment, registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED', appointment=test_visit.appointment, registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
        test_scheduled_model1 = TestScheduledModel1Factory(test_visit=test_visit, f1='No')
        self.assertEqual(RequisitionMetaData.objects.filter(appointment=test_visit.appointment, registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED', appointment=test_visit.appointment, registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
        test_scheduled_model1.f1 = 'Yes'
        test_scheduled_model1.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status='KEYED', appointment=test_visit.appointment, registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)

    def test_base1(self):
        site_rule_groups._registry = {}

        class BaseTestRuleGroupSched(RuleGroup):
            test_rule = RequisitionRule(
                logic=Logic(
                    predicate=(('f1', 'equals', 'No')),
                    consequence='not_required',
                    alternative='new'),
                target_model=['testrequisition'],
                target_requisition_panels=['microtube', 'viral load'])

            class Meta:
                abstract = True

        class TestRuleGroupSched1(BaseTestRuleGroupSched):
            test_rule2 = RequisitionRule(
                logic=Logic(
                    predicate=(('f2', 'equals', 'Yes')),
                    consequence='not_required',
                    alternative='none'),
                target_model=['testrequisition'],
                target_requisition_panels=['microtube', 'viral load'])

            class Meta:
                app_label = 'testing'
                source_fk = (TestVisit, 'test_visit')
                source_model = TestScheduledModel1
        site_rule_groups.register(TestRuleGroupSched1)

        requisition_panel = RequisitionPanel.objects.get(name='Microtube')
        test_panel = TestPanel.objects.get(name=requisition_panel.name)
        test_aliquot_type = TestAliquotType.objects.get(alpha_code='WB')
        test_visit = self.test_visit_factory(appointment=self.appointment)
        #TestRequisitionFactory(test_visit=test_visit, panel=test_panel, aliquot_type=test_aliquot_type)
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
        test_scheduled_model1 = TestScheduledModel1Factory(test_visit=test_visit, f1='No', f2='No')
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
        test_scheduled_model1.f1 = 'Yes'
        test_scheduled_model1.f2 = 'No'
        test_scheduled_model1.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=REQUIRED, registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
        test_scheduled_model1.f1 = 'No'
        test_scheduled_model1.save()
        self.assertEqual(RequisitionMetaData.objects.filter(entry_status=NOT_REQUIRED, registered_subject=self.registered_subject, lab_entry__requisition_panel=requisition_panel).count(), 1)
