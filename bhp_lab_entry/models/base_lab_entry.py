from django.db import models
from edc_lab.lab_clinic_api.models import Panel
from edc_core.bhp_common.choices import YES_NO
from edc_core.bhp_visit.models import BaseWindowPeriodItem
from edc_core.bhp_entry.choices import ENTRY_CATEGORY, ENTRY_WINDOW, ENTRY_STATUS


class BaseLabEntry(BaseWindowPeriodItem):

    # TODO: this needs to be dropped
    #panel = models.ForeignKey(Panel)

    # TODO: this needs to be filled in then renamed as panel
    panel = models.ForeignKey(Panel,
        null=True,
        help_text='This is to replace panel above...')

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
