from django.db import models
from edc.lab.lab_clinic_api.models import Panel
from edc.choices.common import YES_NO
from edc.subject.visit_schedule.models import BaseWindowPeriodItem
from edc.subject.entry.choices import ENTRY_CATEGORY, ENTRY_WINDOW, ENTRY_STATUS


class BaseLabEntry(BaseWindowPeriodItem):

    panel = models.ForeignKey(Panel, null=True)

    entry_order = models.IntegerField()

    required = models.CharField(
        max_length=10,
        choices=YES_NO,
        default='YES')

    entry_category = models.CharField(
        max_length=25,
        choices=ENTRY_CATEGORY,
        default='CLINIC',
        )

    entry_window_calculation = models.CharField(
        max_length=25,
        choices=ENTRY_WINDOW,
        default='VISIT',
        help_text='Base the entry window period on the visit window period or specify a form specific window period',
        )

    default_entry_status = models.CharField(
        max_length=25,
        choices=ENTRY_STATUS,
        default='NEW',
        )

    class Meta:
        abstract = True
