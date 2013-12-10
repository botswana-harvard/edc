from collections import OrderedDict, namedtuple

from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model

from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.lab.lab_clinic_api.models import Panel
from edc.subject.entry.models import Entry, LabEntry

from ..models import MembershipForm, ScheduleGroup, VisitDefinition

EntryTuple = namedtuple('EntryTuple', 'order app_label model_name')
MembershipFormTuple = namedtuple('MembershipFormTuple', 'name model visible')
RequisitionTuple = namedtuple('RequisitionTuple', 'entry_order app_label model_name panel_name panel_edc_name panel_type aliquot_type')
ScheduleGroupTuple = namedtuple('ScheduleTuple', 'name membership_form_name grouping_key comment')


class VisitScheduleConfiguration(object):

    name = 'unnamed visit schedule'
    app_label = None
    membership_forms = OrderedDict()
    schedule_groups = OrderedDict()
    visit_definitions = OrderedDict()

    def __init__(self):
        self.verify()

    def __repr__(self):
        return '{0}.{1}'.format(self.app_label, self.name)

    def verify(self):
        """Verifies some aspects of the the format of the dictionary attributes."""
        for membership_form in self.membership_forms.itervalues():
            if not issubclass(membership_form.__class__, MembershipFormTuple):
                raise ImproperlyConfigured('Visit Schedule Configuration attribute membership_forms '
                                           'must contain instances of the named tuple MembershipFormTuple. '
                                           'Got {0}'.format(membership_form))
        for schedule_group in self.schedule_groups.itervalues():
            if not issubclass(schedule_group.__class__, ScheduleGroupTuple):
                raise ImproperlyConfigured('Visit Schedule Configuration attribute schedule_groups '
                                           'must contain instances of the named tuple ScheduleGroupTuple. '
                                           'Got {0}'.format(schedule_group))
        for name, membership_form in self.membership_forms.iteritems():
            if not name == membership_form.name:
                raise ImproperlyConfigured('Visit Schedule Configuration attribute membership_forms '
                                           'expects each dictionary key {0} to be in it\'s named tuple. '
                                           'Got {1}.'.format(name, membership_form.name))
        for name, schedule_group in self.schedule_groups.iteritems():
            if not name == schedule_group.name:
                raise ImproperlyConfigured('Visit Schedule Configuration attribute schedule_groups '
                                           'expects each dictionary key {0} to be in it\'s named tuple. '
                                           'Got {1}.'.format(name, schedule_group.name))
        for schedule_group_name in self.schedule_groups:
            if schedule_group_name in self.membership_forms:
                raise ImproperlyConfigured('Visit Schedule Configuration attribute schedule_groups '
                                           'cannot have the same name as a membership_form. '
                                           'Got {0} in {1}.'.format(schedule_group_name, self.membership_forms.keys()))
        for schedule_group in self.schedule_groups.itervalues():
            if not schedule_group.membership_form_name in self.membership_forms:
                raise ImproperlyConfigured('Visit Schedule Configuration attribute schedule_groups '
                                           'refers to a membership_form not listed in attribute membership_forms. '
                                           'Got {0} not in {1}.'.format(schedule_group.membership_form_name, self.membership_forms.keys()))
        for visit_definition in self.visit_definitions.itervalues():
            for entry in visit_definition.get('entries'):
                if not get_model(entry.app_label, entry.model_name):
                    raise ImproperlyConfigured('Visit Schedule Configuration attribute entries refers '
                                               'to model {0}.{1} which does not exist.'.format(entry.app_label, entry.model_name))
        for visit_definition in self.visit_definitions.itervalues():
            for requisition in visit_definition.get('requisitions'):
                if not get_model(requisition.app_label, requisition.model_name):
                    raise ImproperlyConfigured('Visit Schedule Configuration attribute requisitions '
                                               'refers to model {0}.{1} which does not exist.'.format(requisition.app_label, requisition.model_name))

    def rebuild(self):
        """Rebuild, WARNING which DELETES meta data."""
        from edc.subject.appointment.models import Appointment
        for code in self.visit_definitions.iterkeys():
            if VisitDefinition.objects.filter(code=code):
                obj = VisitDefinition.objects.get(code=code)
                Entry.objects.filter(visit_definition=obj).delete()
                if not Appointment.objects.filter(visit_definition=obj):
                    obj.delete()
        for schedule_group_name in self.schedule_groups.iterkeys():
            ScheduleGroup.objects.filter(group_name=schedule_group_name).delete()
        for membership_form_name in self.membership_forms.iterkeys():
            MembershipForm.objects.filter(category=membership_form_name).delete()
        self.build()

    def build(self):
        """Builds and / or updates the visit schedule models."""
        for membership_form in self.membership_forms.itervalues():
            if not MembershipForm.objects.filter(category=membership_form.name):
                MembershipForm.objects.create(
                    category=membership_form.name,
                    app_label=membership_form.model._meta.app_label,
                    model_name=membership_form.model._meta.object_name,
                    content_type_map=ContentTypeMap.objects.get(
                        app_label=membership_form.model._meta.app_label,
                        module_name=membership_form.model._meta.object_name.lower()),
                    visible=membership_form.visible)
            else:
                obj = MembershipForm.objects.get(category=membership_form.name)
                obj.app_label = membership_form.model._meta.app_label
                obj.model_name = membership_form.model._meta.object_name
                obj.content_type_map = ContentTypeMap.objects.get(
                    app_label=membership_form.model._meta.app_label,
                    module_name=membership_form.model._meta.object_name.lower())
                obj.visible = membership_form.visible
                obj.save()
        for group_name, schedule_group in self.schedule_groups.iteritems():
            if not ScheduleGroup.objects.filter(group_name=schedule_group.name):
                ScheduleGroup.objects.create(
                    group_name=group_name,
                    membership_form=MembershipForm.objects.get(category=schedule_group.membership_form_name),
                    grouping_key=schedule_group.grouping_key,
                    comment=schedule_group.comment)
            else:
                obj = ScheduleGroup.objects.get(group_name=group_name)
                obj.group_name = group_name
                obj.membership_form = MembershipForm.objects.get(category=schedule_group.membership_form_name)
                obj.grouping_key = schedule_group.grouping_key
                obj.comment = schedule_group.comment
                obj.save()
        for code, visit_definition in self.visit_definitions.iteritems():
            visit_tracking_content_type_map = ContentTypeMap.objects.get(
                app_label=visit_definition.get('visit_tracking_model')._meta.app_label,
                module_name=visit_definition.get('visit_tracking_model')._meta.object_name.lower())
            schedule_group = ScheduleGroup.objects.get(group_name=visit_definition.get('schedule_group'))
            if not VisitDefinition.objects.filter(code=code):
                visit_definition_instance = VisitDefinition.objects.create(
                    code=code,
                    title=visit_definition.get('title'),
                    time_point=visit_definition.get('time_point'),
                    base_interval=visit_definition.get('base_interval'),
                    base_interval_unit=visit_definition.get('base_interval_unit'),
                    lower_window=visit_definition.get('window_lower_bound'),
                    lower_window_unit=visit_definition.get('window_lower_bound_unit'),
                    upper_window=visit_definition.get('window_upper_bound'),
                    upper_window_unit=visit_definition.get('window_upper_bound_unit'),
                    grouping=visit_definition.get('grouping'),
                    visit_tracking_content_type_map=visit_tracking_content_type_map,
                    instruction=visit_definition.get('instructions') or '-',
                    )
            else:
                visit_definition_instance = VisitDefinition.objects.get(code=code)
                visit_definition_instance.code = code
                visit_definition_instance.title = visit_definition.get('title')
                visit_definition_instance.time_point = visit_definition.get('time_point')
                visit_definition_instance.base_interval = visit_definition.get('base_interval')
                visit_definition_instance.base_interval_unit = visit_definition.get('base_interval_unit')
                visit_definition_instance.lower_window = visit_definition.get('window_lower_bound')
                visit_definition_instance.lower_window_unit = visit_definition.get('window_lower_bound_unit')
                visit_definition_instance.upper_window = visit_definition.get('window_upper_bound')
                visit_definition_instance.upper_window_unit = visit_definition.get('window_upper_bound_unit')
                visit_definition_instance.grouping = visit_definition.get('grouping')
                visit_definition_instance.visit_tracking_content_type_map = visit_tracking_content_type_map
                visit_definition_instance.instruction = visit_definition.get('instructions') or '-'
                visit_definition_instance.save()
            visit_definition_instance.schedule_group.add(schedule_group)
            for entry in visit_definition.get('entries'):
                content_type_map = ContentTypeMap.objects.get(app_label=entry.app_label, module_name=entry.model_name.lower())
                if not Entry.objects.filter(app_label=entry.app_label, model_name=entry.model_name.lower(), visit_definition=visit_definition_instance):
                    Entry.objects.create(
                        content_type_map=content_type_map,
                        visit_definition=visit_definition_instance,
                        entry_order=entry.order,
                        app_label=entry.app_label.lower(),
                        model_name=entry.model_name.lower())
                else:
                    obj = Entry.objects.get(app_label=entry.app_label, model_name=entry.model_name.lower(), visit_definition=visit_definition_instance)
                    obj.entry_order = entry.order
                    obj.app_label = entry.app_label.lower()
                    obj.model_name = entry.model_name.lower()
                    obj.save()
            for entry in Entry.objects.filter(visit_definition=visit_definition_instance):
                if (entry.app_label.lower(), entry.model_name.lower()) not in [(item.app_label.lower(), item.model_name.lower()) for item in visit_definition.get('entries')]:
                    entry.delete()
            for requisition in visit_definition.get('requisitions'):
                if not Panel.objects.filter(name=requisition.panel_name):
                    panel = Panel.objects.create(name=requisition.panel_name, edc_name=requisition.panel_edc_name, panel_type=requisition.panel_type)
                    #panel.aliquot_type.add(requisition.aliquot_type)
                else:
                    Panel.objects.filter(name=requisition.panel_name).update(name=requisition.panel_name, edc_name=requisition.panel_edc_name, panel_type=requisition.panel_type)
                    panel = Panel.objects.get(name=requisition.panel_name)
                    panel.aliquot_type.clear()
                    #panel.aliquot_type.add(requisition.aliquot_type)

                if not LabEntry.objects.filter(panel=panel, app_label=requisition.app_label, model_name=requisition.model_name, visit_definition=visit_definition_instance):
                    LabEntry.objects.create(
                        app_label=requisition.app_label,
                        model_name=requisition.model_name,
                        panel=panel,
                        visit_definition=visit_definition_instance,
                        entry_order=requisition.entry_order,
                        )
                else:
                    LabEntry.objects.filter(panel=panel, app_label=requisition.app_label, model_name=requisition.model_name, visit_definition=visit_definition_instance).update(entry_order=requisition.entry_order)
            for requisition in LabEntry.objects.filter(visit_definition=visit_definition_instance):
                if (requisition.app_label, requisition.model_name) not in [(item.app_label, item.model_name) for item in visit_definition.get('requisitions')]:
                    requisition.delete()