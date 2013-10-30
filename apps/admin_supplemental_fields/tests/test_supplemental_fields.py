from datetime import datetime
from uuid import uuid4

from django.contrib import admin
from django.contrib.auth.models import User
from django.db import models
from django.test import TestCase
from django.test.client import RequestFactory

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.tests.factories import StudySpecificFactory, StudySiteFactory
from edc.subject.appointment.models import Appointment
from edc.subject.appointment.tests.factories import ConfigurationFactory
from edc.subject.consent.tests.factories import ConsentCatalogueFactory
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.tests.factories import MembershipFormFactory, ScheduleGroupFactory, VisitDefinitionFactory
from edc.subject.visit_tracking.admin import BaseVisitTrackingModelAdmin
from edc.testing.forms import TestScheduledModelForm
from edc.testing.models import TestScheduledModel, TestVisit, TestConsentWithMixin
from edc.testing.tests.factories import TestScheduledModelFactory, TestVisitFactory, TestConsentWithMixinFactory

from ..admin import SupplementalModelAdminMixin
from ..classes import SupplementalFields
from ..models import ExcludedHistory


class TestScheduledModelAdmin(SupplementalModelAdminMixin, BaseVisitTrackingModelAdmin):
    visit_model = TestVisit
    form = TestScheduledModelForm
    supplemental_fields = SupplementalFields(('f2', 'f3', 'f4'), p=0.9, group='TEST', grouping_field='test_visit')
    fields = ('report_datetime', 'f1', 'f2', 'f3', 'f4')

    def has_add_permission(self, request):
        return True

    def has_change_permission(self, request, obj):
        return True

admin.site.register(TestScheduledModel, TestScheduledModelAdmin)


class TestSupplementalFields(TestCase):

    app_label = 'testing'

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(username='erikvw', email='erik@doghouse.com', password='bad_dog')
        site_lab_tracker.autodiscover()
        study_specific = StudySpecificFactory()
        StudySiteFactory()
        ConfigurationFactory()
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        content_type_map = ContentTypeMap.objects.get(content_type__model='TestConsentWithMixin'.lower())
        ConsentCatalogueFactory(
            name=self.app_label,
            consent_type='study',
            content_type_map=content_type_map,
            version=1,
            start_datetime=study_specific.study_start_datetime,
            end_datetime=datetime(datetime.today().year + 5, 1, 1),
            add_for_app=self.app_label)
        membership_form = MembershipFormFactory(content_type_map=content_type_map)
        schedule_group = ScheduleGroupFactory(membership_form=membership_form, group_name='test', grouping_key='TEST')
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='testvisit')
        visit_definition = VisitDefinitionFactory(code='T0', title='T0', grouping='subject', visit_tracking_content_type_map=visit_tracking_content_type_map)
        visit_definition.schedule_group.add(schedule_group)
        subject_consent = TestConsentWithMixinFactory()
        self.registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_consent.subject_identifier)
        self.consent = TestConsentWithMixin.objects.get(registered_subject=self.registered_subject)
        appointment = Appointment.objects.get(registered_subject=self.registered_subject)
        self.test_visit = TestVisitFactory(appointment=appointment)

    def test_init(self):
        """only accepts a list or tuple for fields"""
        fields = 1
        self.assertRaises(AttributeError, SupplementalFields, fields, 0.1)
        fields = 'field'
        self.assertRaises(AttributeError, SupplementalFields, fields, 0.1)
        fields = ['field1', 'field2', 'field3']
        self.assertTrue(isinstance(SupplementalFields(fields, 0.1), SupplementalFields))
        fields = ('field1', 'field2', 'field3')
        self.assertTrue(isinstance(SupplementalFields(fields, 0.1), SupplementalFields))

    def test_init2(self):
        fields = ['field1', 'field2', 'field3']
        probability = 0.9
        group = 'GROUP'
        grouping_field = 'test_visit'

        supplemental_fields = SupplementalFields(fields, p=probability, group=group, grouping_field=grouping_field)

        self.assertEqual(fields, supplemental_fields.get_supplemental_fields())
        self.assertEqual(probability, supplemental_fields.get_probability_to_include())
        self.assertEqual(group, supplemental_fields.get_group())
        self.assertEqual(grouping_field, supplemental_fields.get_grouping_field())

    def test_update_history_before_save1(self):
        """creates a history record if using a grouping field on ADD."""
        for adm in admin.site._registry.itervalues():
            if isinstance(adm, TestScheduledModelAdmin):
                self.assertEqual(ExcludedHistory.objects.all().count(), 0)
                fake_visit_pk = unicode(uuid4())
                request = self.factory.get('/', data={'visit_attr': 'test_visit', 'test_visit': fake_visit_pk})
                request.user = self.user
                adm.supplemental_fields.set_probability_to_include(0.0)  # so it will exclude the supplemental fields
                adm.add_view(request)
                self.assertEqual(adm.get_grouping_field(), 'test_visit')
                self.assertEqual(adm.get_grouping_pk(), fake_visit_pk)
                self.assertEqual(adm.get_exclude_fields(), ('f2', 'f3', 'f4'))
                self.assertEqual(ExcludedHistory.objects.all().count(), 1)

    def test_update_history_before_save2(self):
        """does not creates a history record if using a grouping field on ADD if no exclude fields."""
        for adm in admin.site._registry.itervalues():
            if isinstance(adm, TestScheduledModelAdmin):
                self.assertEqual(ExcludedHistory.objects.all().count(), 0)
                fake_visit_pk = unicode(uuid4())
                request = self.factory.get('/', data={'visit_attr': 'test_visit', 'test_visit': fake_visit_pk})
                request.user = self.user
                adm.supplemental_fields.set_probability_to_include(1.0)  # so the fields will be included
                adm.add_view(request)
                self.assertEqual(adm.get_grouping_field(), 'test_visit')
                self.assertEqual(adm.get_grouping_pk(), fake_visit_pk)
                self.assertEqual(adm.get_exclude_fields(), '')
                self.assertEqual(ExcludedHistory.objects.all().count(), 1)

    def test_update_history_after_save1(self):
        """Creates a history record if using a grouping field on CHANGE if no exclude fields."""
        for adm in admin.site._registry.itervalues():
            if isinstance(adm, TestScheduledModelAdmin):
                test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)

                self.assertEqual(ExcludedHistory.objects.all().count(), 0)

                request = self.factory.get('/', data={'visit_attr': 'test_visit', 'test_visit': self.test_visit.pk})
                request.user = self.user

                # set p=0.0 so the questions will be excluded from the form
                adm.supplemental_fields.set_probability_to_include(0.0)

                # call change view to fake a change through admin
                adm.change_view(request, test_scheduled_model.pk)

                self.assertEqual(adm.get_grouping_field(), 'test_visit')
                self.assertEqual(adm.get_grouping_pk(), self.test_visit.pk)
                self.assertEqual(adm.get_exclude_fields(), ('f2', 'f3', 'f4'))

                # modeladmin has not called save_model to update the model_pk in history
                self.assertEqual(ExcludedHistory.objects.filter(model_pk=test_scheduled_model.pk).count(), 0)

                # but history is created for the "group" via this model linked by the grouping pk.
                self.assertEqual(ExcludedHistory.objects.filter(grouping_pk=adm.get_grouping_pk()).count(), 1)

    def test_update_history_after_save2(self):
        """creates a history record if using a grouping field on CHANGE."""
        for adm in admin.site._registry.itervalues():
            if isinstance(adm, TestScheduledModelAdmin):
                self.assertEqual(ExcludedHistory.objects.all().count(), 0)

                request = self.factory.get('/', data={'visit_attr': 'test_visit', 'test_visit': self.test_visit.pk})
                request.user = self.user

                # set p=1 so that fields will be included on the form
                adm.supplemental_fields.set_probability_to_include(1.0)

                test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)

                adm.change_view(request, test_scheduled_model.pk)

                self.assertEqual(adm.get_grouping_field(), 'test_visit')
                self.assertEqual(adm.get_grouping_pk(), self.test_visit.pk)
                self.assertEqual(adm.get_exclude_fields(), '')

                self.assertEqual(ExcludedHistory.objects.all().count(), 1)

    def test_uses_grouping_from_history1(self):
        """selects the excluded fields a model of the same group has history"""
        for adm in admin.site._registry.itervalues():
            if isinstance(adm, TestScheduledModelAdmin):
                self.assertEqual(ExcludedHistory.objects.all().count(), 0)

                test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)

                # create a fake history for a model in the same group using the same grouping pk
                ExcludedHistory.objects.create(excluded_fields='', group='TEST', grouping_field='test_visit', grouping_pk=self.test_visit.pk, app_label='testing', object_name='some_other_model1')

                request = self.factory.get('/', data={'visit_attr': 'test_visit', 'test_visit': self.test_visit.pk})
                request.user = self.user

                # set p=0 so that it excludes the fields from the form
                adm.supplemental_fields.set_probability_to_include(0.0)

                # fake a change
                adm.change_view(request, test_scheduled_model.pk)

                # but since we retrieved from the history, should ignore p and not exclude any fields
                self.assertEqual(adm.get_exclude_fields(), '')

                self.assertEqual(ExcludedHistory.objects.filter(excluded_fields='').count(), 2)

    def test_uses_grouping_from_history2(self):
        """selects the excluded fields for a model using the history of another model in the group"""
        for adm in admin.site._registry.itervalues():
            if isinstance(adm, TestScheduledModelAdmin):
                self.assertEqual(ExcludedHistory.objects.all().count(), 0)

                test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)

                # create more than one fake history for a model in the same group using the same grouping pk
                ExcludedHistory.objects.create(excluded_fields='f2,f3,f4', group='TEST', grouping_field='test_visit', grouping_pk=self.test_visit.pk, app_label='testing', object_name='some_other_model1')
                ExcludedHistory.objects.create(excluded_fields='f2,f3,f4', group='TEST', grouping_field='test_visit', grouping_pk=self.test_visit.pk, app_label='testing', object_name='some_other_model2')
                ExcludedHistory.objects.create(excluded_fields='f2,f3,f4', group='TEST', grouping_field='test_visit', grouping_pk=self.test_visit.pk, app_label='testing', object_name='some_other_model3')

                request = self.factory.get('/', data={'visit_attr': 'test_visit', 'test_visit': self.test_visit.pk})
                request.user = self.user

                # set p=0 so that it DOES NOT exclude the fields from the form
                adm.supplemental_fields.set_probability_to_include(1.0)

                # fake a change
                adm.change_view(request, test_scheduled_model.pk)

                # but since we retrieved from the history, should ignore p and exclude the supplemental fields
                self.assertEqual(adm.get_exclude_fields(), ('f2', 'f3', 'f4'),)

                self.assertEqual(ExcludedHistory.objects.filter(excluded_fields='f2,f3,f4').count(), 4)

    def test_uses_grouping_from_history3(self):
        """selects the excluded fields a model of the same group that has history"""
        for adm in admin.site._registry.itervalues():
            if isinstance(adm, TestScheduledModelAdmin):
                self.assertEqual(ExcludedHistory.objects.all().count(), 0)

                test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)

                # create more than one fake history for a model in the same group using the same grouping pk
                ExcludedHistory.objects.create(group='TEST', grouping_field='test_visit', grouping_pk=self.test_visit.pk, app_label='testing', object_name='some_other_model1')
                ExcludedHistory.objects.create(group='TEST', grouping_field='test_visit', grouping_pk=self.test_visit.pk, app_label='testing', object_name='some_other_model2')
                ExcludedHistory.objects.create(group='TEST', grouping_field='test_visit', grouping_pk=self.test_visit.pk, app_label='testing', object_name='some_other_model3')

                request = self.factory.get('/', data={'visit_attr': 'test_visit', 'test_visit': self.test_visit.pk})
                request.user = self.user

                # set p=0 so that it excludes the fields from the form
                adm.supplemental_fields.set_probability_to_include(0.0)

                # fake a change
                adm.change_view(request, test_scheduled_model.pk)

                # but since we retrieved from the history, should ignore p and not exclude any fields
                self.assertEqual(adm.get_exclude_fields(), '')

                self.assertEqual(ExcludedHistory.objects.filter(excluded_fields='').count(), 4)

    def test_uses_grouping_from_history4(self):
        """selects the excluded fields a model of the same group that has history"""
        for adm in admin.site._registry.itervalues():
            if isinstance(adm, TestScheduledModelAdmin):
                self.assertEqual(ExcludedHistory.objects.all().count(), 0)

                test_scheduled_model = TestScheduledModelFactory(test_visit=self.test_visit)

                request = self.factory.get('/', data={'visit_attr': 'test_visit', 'test_visit': self.test_visit.pk})
                request.user = self.user

                # set p=0 so that it excludes the fields from the form
                adm.supplemental_fields.set_probability_to_include(0.0)

                # fake a change
                adm.change_view(request, test_scheduled_model.pk)

                # a history entry is made
                self.assertEqual(ExcludedHistory.objects.filter(grouping_pk=self.test_visit.pk).count(), 1)
                # but since we have not called save_model, the pk has not been updated
                self.assertEqual(ExcludedHistory.objects.filter(model_pk=test_scheduled_model.pk).count(), 0)

                form = adm.get_form(request, test_scheduled_model)

                adm.save_model(request, test_scheduled_model, form, True)

                # having claeed save_model, pk is now updated
                self.assertEqual(ExcludedHistory.objects.filter(model_pk=test_scheduled_model.pk).count(), 1)

                # and it was updated, not inserted, so still have one history
                self.assertEqual(ExcludedHistory.objects.all().count(), 1)

    def test_check_supplemental_in_original(self):
        fields = ('field1', 'field2', 'field7')
        supplemental_fields = SupplementalFields(fields, 0.231)
        supplemental_fields.set_original_model_admin_fields(('field1', 'field2', 'field3', 'field4', 'field5'))
        self.assertRaises(AttributeError, supplemental_fields.check_supplemental_in_original)
        fields = ('field1', 'field2', 'field3')
        supplimental_fields = SupplementalFields(fields, 0.231)
        supplimental_fields.set_original_model_admin_fields(('field1', 'field2', 'field3', 'field4', 'field5'))
        self.assertTrue(supplimental_fields.check_supplemental_in_original())

    def test_check_supplemental_field_attrs(self):
        fields = ('field1', 'field2', 'field3')
        supplemental_fields = SupplementalFields(fields, 0.231)

        class BadModel1(models.Model):
            field1 = models.IntegerField(editable=False)
            field2 = models.IntegerField()
            field3 = models.IntegerField()
            field4 = models.IntegerField()
            field5 = models.IntegerField()

        supplemental_fields.set_model(BadModel1)
        self.assertRaises(AttributeError, supplemental_fields.check_supplemental_field_attrs)

        class BadModel2(models.Model):
            field1 = models.IntegerField()
            field2 = models.IntegerField()
            field3 = models.IntegerField()
            field4 = models.IntegerField()
            field5 = models.IntegerField()

        supplemental_fields.set_model(BadModel2)
        self.assertRaises(AttributeError, supplemental_fields.check_supplemental_field_attrs)

        class BadModel3(models.Model):
            field1 = models.IntegerField(null=True, editable=False)
            field2 = models.IntegerField()
            field3 = models.IntegerField()
            field4 = models.IntegerField()
            field5 = models.IntegerField()

        supplemental_fields.set_model(BadModel3)
        self.assertRaises(AttributeError, supplemental_fields.check_supplemental_field_attrs)

        class GoodModel(models.Model):
            field1 = models.IntegerField(null=True, blank=False)
            field2 = models.IntegerField(null=True, editable=True)
            field3 = models.IntegerField(null=True)
            field4 = models.IntegerField(null=True)
            field5 = models.IntegerField(null=True)

        supplemental_fields.set_model(GoodModel)
        self.assertTrue(supplemental_fields.check_supplemental_field_attrs())

    def test_p1(self):
        sf = SupplementalFields(('f3', 'f4'), p=0.1)
        seq = sf.get_probability_as_sequence()
        self.assertEqual(len(seq), 1000)
        self.assertEqual(seq.count(0), 100)
        self.assertEqual(seq.count(1), 900)

    def test_p2(self):
        sf = SupplementalFields(('f3', 'f4'), p=0.5)
        seq = sf.get_probability_as_sequence()
        self.assertEqual(len(seq), 1000)
        self.assertEqual(seq.count(0), 500)
        self.assertEqual(seq.count(1), 500)

    def test_p3(self):
        sf = SupplementalFields(('f3', 'f4'), p=0.135)
        seq = sf.get_probability_as_sequence()
        self.assertEqual(len(seq), 1000)
        self.assertEqual(seq.count(0), 135)
        self.assertEqual(seq.count(1), 865)

    def test_p4(self):
        self.assertRaises(AttributeError, SupplementalFields, "X", p=0.1)
        self.assertRaises(AttributeError, SupplementalFields, ('f3', 'f4'), p=1)
        self.assertRaises(AttributeError, SupplementalFields, ('f3', 'f4'), p=0.1355)

    def test_5(self):
        """test that ModelAdmin fields is correctly reset after use."""
        pass

#     def test_p5(self):
#         P = 0
#         INC = 1
#         EXC = 2
#         for opt in [(0.135, 135, 865), (0.5, 500, 500), (0.75, 750, 250)]:
#             print 'p={0} include(0)={1} exclude(1)={2}'.format(*opt)
#             sf = SupplementalFields(('f3', 'f4'), p=opt[P])
#             self.assertEqual(sf._get_probability_as_sequence().count(0), opt[INC])
#             self.assertEqual(sf._get_probability_as_sequence().count(1), opt[EXC])
#             zero = []
#             one = []
#             for j in range(0, 1000):
#                 lst = []
#                 for i in range(0, 1000):
#                     fields, exclude_fields = sf.choose_fields(('f1', 'f2', 'f3', 'f4', 'f5'), TestModel())
#                     if fields == ('f1', 'f2', 'f3', 'f4', 'f5') and not exclude_fields:
#                         # supp fields were not excluded
#                         lst.append(0)
#                     elif fields == ('f1', 'f2', 'f5') and exclude_fields == ('f3', 'f4'):
#                         # supp fields were excluded
#                         lst.append(1)
#                     else:
#                         lst.append(2)
#                         print '  fields={0}'.format(fields)
#                         print '  exclude_fields={0}'.format(exclude_fields)
#                 zero.append(lst.count(0))
#                 one.append(lst.count(1))
#                 self.assertEqual(lst.count(2), 0)
#                 #if opt[P] > 0.5:
#                 #    self.assertGreater(lst.count(0), lst.count(1))
#                 #elif opt[P] < 0.5:
#                 #    self.assertLess(lst.count(0), lst.count(1))
#                 #else:
#                 #    pass
#                 #print '    0 -> {0} < {1} < {2}'.format(opt[INC] - (opt[INC] * (opt[P] * 2)), lst.count(0), opt[INC] + (opt[INC] * (opt[P] * 2)))
#                 #self.assertTrue(opt[INC] - (opt[INC] * (opt[P] * 2)) < lst.count(0) < opt[INC] + (opt[INC] * (opt[P] * 2)))
#                 #print '    1 -> {0} < {1} < {2}'.format(opt[EXC] - (opt[EXC] * (opt[P] * 2)), lst.count(1), opt[EXC] + (opt[EXC] * (opt[P] * 2)))
#                 #self.assertTrue(opt[EXC] - (opt[EXC] * (opt[P] * 2)) < lst.count(1) < opt[EXC] + (opt[EXC] * (opt[P] * 2)))
#                 #self.assertTrue(lst.count(0) in range(110, 155), lst.count(0))
#                 #self.assertTrue(lst.count(1) in range(850, 883), lst.count(1))
#             print '  Included mean={0} std={1}, n={2}'.format(numpy.mean(zero), numpy.std(zero), len(zero))
#             print '  Excluded mean={0} std={1}, n={2} '.format(numpy.mean(one), numpy.std(one), len(one))

