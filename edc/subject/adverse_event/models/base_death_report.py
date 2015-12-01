from django.db import models

from edc_constants.choices import YES_NO
from edc.subject.code_lists.models import DxCode

from .base_death import BaseDeath


class BaseDeathReport(BaseDeath):

    """
    Death form / AF005
    """
    illness_duration = models.IntegerField(
        verbose_name="Duration of acute illness directly causing death   ",
        help_text="in days (If unknown enter -1)",
        )

    perform_autopsy = models.CharField(
        max_length=3,
        choices=YES_NO,
        verbose_name="Will an autopsy be performed later  ",
        help_text="",
        )

    dx_code = models.ForeignKey(DxCode,
        max_length=25,
        verbose_name="Please code the cause of death as one of the following:",
        help_text="Use diagnosis code from Diagnosis Reference Listing",
        )
    
    dx_code_other = OtherCharField(
        verbose_name="if other specify...",
        blank=True,
        null=True,
    )

    class Meta:
        abstract = True
