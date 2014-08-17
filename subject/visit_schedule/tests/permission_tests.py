from django.test import TestCase
from django.db.models import get_app, get_models
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.subject.entry.models import Entry
from edc.core.bhp_content_type_map.models import ContentTypeMap

from ..models import VisitDefinition
from ..classes import Permissions
from .factories import VisitDefinitionFactory


class PermissionTests(TestCase):

    def setUp(self):
        content_type_map_helper = ContentTypeMapHelper()
        content_type_map_helper.populate()
        content_type_map_helper.sync()
        visit_tracking_content_type_map = ContentTypeMap.objects.get(content_type__model='testvisit')
        visit_definition = VisitDefinitionFactory(code='T0', visit_tracking_content_type_map=visit_tracking_content_type_map)
        for index, content_type in enumerate(ContentType.objects.filter(app_label='testing')):
            model = content_type.model_class()
            if 'entry_meta_data_manager' in dir(model):
                content_type_map = ContentTypeMap.objects.get(content_type=content_type)
                Entry.objects.create(visit_definition=visit_definition, content_type_map=content_type_map, entry_order=index)
        visit_definition = VisitDefinitionFactory(code='T1', visit_tracking_content_type_map=visit_tracking_content_type_map)
        for index, content_type in enumerate(ContentType.objects.filter(app_label='testing')[2:]):
            model = content_type.model_class()
            if 'entry_meta_data_manager' in dir(model):
                content_type_map = ContentTypeMap.objects.get(content_type=content_type)
                Entry.objects.create(visit_definition=visit_definition, content_type_map=content_type_map, entry_order=index)

        self.group = Group.objects.create(name='field_staff')

    def test_adds_permissions1(self):
        permissions = Permissions('field_staff', ['add'], visit_definition_codes=['T0'])
        permissions.replace()
        group = Group.objects.get(name='field_staff')
        self.assertGreater(group.permissions.all().count(), 0)

    def test_adds_permissions2(self):
        """Adds permissions to the group for just add."""
        permissions = Permissions('field_staff', ['add'], visit_definition_codes=['T0'])
        permissions.replace()
        group = Group.objects.get(name='field_staff')
        self.assertGreater(group.permissions.filter(codename__icontains='add_').count(), 0)
        self.assertEqual(group.permissions.filter(codename__icontains='change_').count(), 0)
        self.assertEqual(group.permissions.filter(codename__icontains='delete_').count(), 0)

    def test_adds_permissions3(self):
        """Adds permissions to the group for both add and change."""
        codes = ['T0']
        visit_definitions = VisitDefinition.objects.filter(code__in=codes)
        entry_count = Entry.objects.filter(visit_definition__in=visit_definitions).count()
        permissions = Permissions('field_staff', ['add', 'change'], visit_definition_codes=codes)
        permissions.replace()
        group = Group.objects.get(name='field_staff')
        self.assertEqual(group.permissions.filter(codename__icontains='add_').count(), entry_count)
        self.assertEqual(group.permissions.filter(codename__icontains='change_').count(), entry_count)
        self.assertEqual(group.permissions.filter(codename__icontains='delete_').count(), 0)

    def test_adds_permissions4(self):
        """Adds permissions for visit T0 to the group for add and change, delete."""
        codes = ['T0']
        visit_definitions = VisitDefinition.objects.filter(code__in=codes)
        entry_count = Entry.objects.filter(visit_definition__in=visit_definitions).count()
        permissions = Permissions('field_staff', ['add', 'change', 'delete'], visit_definition_codes=codes)
        permissions.replace()
        group = Group.objects.get(name='field_staff')
        self.assertEqual(group.permissions.filter(codename__icontains='add_').count(), entry_count)
        self.assertEqual(group.permissions.filter(codename__icontains='change_').count(), entry_count)
        self.assertEqual(group.permissions.filter(codename__icontains='delete_').count(), entry_count)

    def test_adds_permissions5(self):
        """Adds permissions for another visit, T1, for add, change and delete."""
        codes = ['T1']
        visit_definitions = VisitDefinition.objects.filter(code__in=codes)
        entry_count = Entry.objects.filter(visit_definition__in=visit_definitions).count()
        permissions = Permissions('field_staff', ['add', 'change', 'delete'], visit_definition_codes=codes)
        permissions.replace()
        group = Group.objects.get(name='field_staff')
        self.assertEqual(group.permissions.filter(codename__icontains='add_').count(), entry_count)
        self.assertEqual(group.permissions.filter(codename__icontains='change_').count(), entry_count)
        self.assertEqual(group.permissions.filter(codename__icontains='delete_').count(), entry_count)

    def test_adds_permissions6(self):
        """Adds permissions for both visits, T0 and T1, to the group for both add and change and delete and does not duplicate."""
        codes = ['T0', 'T1']
        visit_definitions = VisitDefinition.objects.filter(code__in=codes)
        entries = Entry.objects.filter(visit_definition__in=visit_definitions)
        entry_count = len(list(set([entry.content_type_map.content_type_id for entry in entries])))
        permissions = Permissions('field_staff', ['add', 'change', 'delete'], visit_definition_codes=codes)
        permissions.replace()
        group = Group.objects.get(name='field_staff')
        self.assertEqual(group.permissions.filter(codename__icontains='add_').count(), entry_count)
        self.assertEqual(group.permissions.filter(codename__icontains='change_').count(), entry_count)
        self.assertEqual(group.permissions.filter(codename__icontains='delete_').count(), entry_count)

    def test_adds_permissions7(self):
        """Creates a group if it does not exist."""
        codes = ['T0']
        permissions = Permissions('field_staff_team', ['add'], visit_definition_codes=codes)
        permissions.replace()
        group = Group.objects.get(name='field_staff_team')
        self.assertGreater(group.permissions.all().count(), 0)

    def test_adds_permissions8(self):
        """Adds permissions for all models in the app"""
        permissions = Permissions('field_staff_team', ['add'], app_label='testing')
        permissions.replace()
        group = Group.objects.get(name='field_staff_team')
        app = get_app('testing')
        models = get_models(app)
        self.assertEquals(group.permissions.all().count(), len(models))

    def test_adds_permissions9(self):
        """Adds permissions for specified list of models in the app."""
        permissions = Permissions('field_staff', ['add', 'change'], app_label='testing', models=['testvisit', 'TestScheduledModel'])
        permissions.replace()
        self.assertEqual(self.group.permissions.filter(codename='add_testvisit').count(), 1)
        self.assertEqual(self.group.permissions.filter(codename='add_testscheduledmodel').count(), 1)
        self.assertEqual(self.group.permissions.filter(codename='change_testvisit').count(), 1)
        self.assertEqual(self.group.permissions.filter(codename='change_testscheduledmodel').count(), 1)

    def test_adds_permissions10(self):
        """Raises error if model not in app"""
        self.assertRaises(AttributeError, Permissions, 'field_staff', ['add', 'change'], app_label='testing', models=['testvisit', 'BadDogModel'])
