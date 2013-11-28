from collections import OrderedDict

from edc.subject.visit_schedule.classes import VisitScheduleConfiguration, site_visit_schedules, RequisitionTuple

from ..models import TestVisit, TestConsentWithMixin


class TestVisitSchedule(VisitScheduleConfiguration):

    app_label = 'testing'
    # membership forms
    # see edc.subject.visit_schedule.models.membership_forms
    membership_forms = OrderedDict({
        'schedule-1': ('schedule-1', TestConsentWithMixin, True),
        })

    # schedule groups
    # see edc.subject.visit_schedule.models.schedule_groups
    # (group_name, membership_form, grouping_key, comment)
    schedule_groups = OrderedDict({
        'schedule-1': ('schedule-1', 'schedule-1', None, None),
        })

    # visit_schedule
    # see edc.subject.visit_schedule.models.visit_defintion
    visit_definitions = OrderedDict(
        {'1000': {
            'title': '1000',
            'time_point': 0,
            'base_interval': 0,
            'base_interval_unit': 'D',
            'window_lower_bound': 0,
            'window_lower_bound_unit': 'D',
            'window_upper_bound': 0,
            'window_upper_bound_unit': 'D',
            'grouping': None,
            'visit_tracking_model': TestVisit,
            'schedule_group': 'schedule-1',
            'instructions': None,
            'requisitions': (
                # (entry_order, app_label, model_name, panel.name, panel.edc_name, panel.panel_type, aliquot_type)
                RequisitionTuple(10L, u'testing', u'testrequisition', 'Research Blood Draw', 'Research Blood Draw', 'TEST', 'WB'),
                RequisitionTuple(20L, u'testing', u'testrequisition', 'Viral Load', 'Viral Load', 'TEST', 'WB'),
                RequisitionTuple(30L, u'testing', u'testrequisition', 'Microtube', 'Microtube', 'STORAGE', 'WB'),
                ),
            'entries': (
                (10L, u'testing', u'TestScheduledModel1'),
                (20L, u'testing', u'TestScheduledModel2'),
                (30L, u'testing', u'TestScheduledModel3'),
            )}
        }
    )

#site_visit_schedules.register(TestVisitSchedule)
