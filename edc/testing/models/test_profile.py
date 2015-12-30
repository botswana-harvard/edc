from django.db import models

from edc_lab.lab_profile.models import BaseProfile
from edc_lab.lab_profile.models import BaseProfileItem

from .test_aliquot_type import TestAliquotType


class TestProfile(BaseProfile):

    aliquot_type = models.ForeignKey(TestAliquotType,
        verbose_name='Source aliquot type')

    class Meta:
        app_label = 'testing'


class TestProfileItem(BaseProfileItem):

    profile = models.ForeignKey(TestProfile)

    aliquot_type = models.ForeignKey(TestAliquotType)

    class Meta:
        app_label = 'testing'
