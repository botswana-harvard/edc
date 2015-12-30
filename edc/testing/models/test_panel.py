from django.db import models
from edc_lab.lab_clinic_api.choices import PANEL_TYPE
from edc_lab.lab_clinic_api.models import TestCode


from lis.specimen.lab_panel.models import BasePanel

from .test_aliquot_type import TestAliquotType


class TestPanel(BasePanel):

    test_code = models.ManyToManyField(TestCode, null=True, blank=True, related_name='++')

    aliquot_type = models.ManyToManyField(TestAliquotType,
        help_text='Choose all that apply',)

    panel_type = models.CharField(max_length=15, choices=PANEL_TYPE, default='TEST')

    objects = models.Manager()

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'testing'
