from collections import OrderedDict

from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.subject.entry.models import Entry

from ..models import MembershipForm, ScheduleGroup, VisitDefinition


class VisitScheduleConfiguration(object):

    app_label = None
    membership_forms = OrderedDict()
    schedule_groups = OrderedDict()
    visit_definitions = OrderedDict()

    def rebuild(self):
        from edc.subject.appointment.models import Appointment
        for code in self.visit_definitions.iterkeys():
            if VisitDefinition.objects.filter(code=code):
                obj = VisitDefinition.objects.get(code=code)
                Entry.objects.filter(visit_definition=obj).delete()
                if not Appointment.objects.filter(visit_definition=obj):
                    obj.delete()
        for group_name in self.schedule_groups.iterkeys():
            ScheduleGroup.objects.filter(group_name=group_name).delete()
        for category in self.membership_forms.iterkeys():
            MembershipForm.objects.filter(category=category).delete()
        self.build()

    def build(self):
        """Builds and / or updates the visit schedule models."""
        for category, definition in self.membership_forms.iteritems():
            if not MembershipForm.objects.filter(category=category):
                MembershipForm.objects.create(
                    category=category,
                    app_label=definition[1]._meta.app_label,
                    model_name=definition[1]._meta.object_name,
                    content_type_map=ContentTypeMap.objects.get(app_label=definition[1]._meta.app_label, module_name=definition[1]._meta.object_name.lower()),
                    visible=definition[2])
            else:
                obj = MembershipForm.objects.get(category=category)
                obj.app_label = definition[1]._meta.app_label
                obj.model_name = definition[1]._meta.object_name
                obj.content_type_map = ContentTypeMap.objects.get(app_label=definition[1]._meta.app_label, module_name=definition[1]._meta.object_name.lower())
                obj.visible = definition[2]
                obj.save()
        for group_name, definition in self.schedule_groups.iteritems():
            if not ScheduleGroup.objects.filter(group_name=group_name):
                ScheduleGroup.objects.create(
                    group_name=group_name,
                    membership_form=MembershipForm.objects.get(category=definition[1]),
                    grouping_key=definition[2],
                    comment=definition[3])
            else:
                obj = ScheduleGroup.objects.get(group_name=group_name)
                obj.group_name = group_name
                obj.membership_form = MembershipForm.objects.get(category=definition[1])
                obj.grouping_key = definition[2]
                obj.comment = definition[3]
                obj.save()
        for code, definition in self.visit_definitions.iteritems():
            visit_tracking_content_type_map = ContentTypeMap.objects.get(app_label=definition.get('visit_tracking_model')._meta.app_label, module_name=definition.get('visit_tracking_model')._meta.object_name.lower())
            schedule_group = ScheduleGroup.objects.get(group_name=definition.get('schedule_group'))
            if not VisitDefinition.objects.filter(code=code):
                visit_definition = VisitDefinition.objects.create(
                    code=code,
                    title=definition.get('title'),
                    time_point=definition.get('time_point'),
                    base_interval=definition.get('base_interval'),
                    base_interval_unit=definition.get('base_interval_unit'),
                    lower_window=definition.get('window_lower_bound'),
                    lower_window_unit=definition.get('window_lower_bound_unit'),
                    upper_window=definition.get('window_upper_bound'),
                    upper_window_unit=definition.get('window_upper_bound_unit'),
                    grouping=definition.get('grouping'),
                    visit_tracking_content_type_map=visit_tracking_content_type_map,
                    instruction=definition.get('instructions') or '-',
                    )
            else:
                visit_definition = VisitDefinition.objects.get(code=code)
                visit_definition.code = code
                visit_definition.title = definition.get('title')
                visit_definition.time_point = definition.get('time_point')
                visit_definition.base_interval = definition.get('base_interval')
                visit_definition.base_interval_unit = definition.get('base_interval_unit')
                visit_definition.lower_window = definition.get('window_lower_bound')
                visit_definition.lower_window_unit = definition.get('window_lower_bound_unit')
                visit_definition.upper_window = definition.get('window_upper_bound')
                visit_definition.upper_window_unit = definition.get('window_upper_bound_unit')
                visit_definition.grouping = definition.get('grouping')
                visit_definition.visit_tracking_content_type_map = visit_tracking_content_type_map
                visit_definition.instruction = definition.get('instructions') or '-'
                visit_definition.save()
            visit_definition.schedule_group.add(schedule_group)
            for entry in definition.get('entries'):
                content_type_map = ContentTypeMap.objects.get(app_label=entry[1], module_name=entry[2].lower())
                if not Entry.objects.filter(app_label=entry[1], model_name=entry[2]):
                    Entry.objects.create(
                        content_type_map=content_type_map,
                        visit_definition=visit_definition,
                        entry_order=entry[0],
                        app_label=entry[1],
                        model_name=entry[2])
                else:
                    obj = Entry.objects.get(content_type_map=content_type_map, visit_definition=visit_definition)
                    obj.entry_order = entry[0]
                    obj.app_label = entry[1]
                    obj.model_name = entry[2]
                    obj.save()
