from django.db import models

from ..managers import TestRegistrationManager

from edc_offstudy.models import OffStudyMixin


class TestRegistration(OffStudyMixin, models.Model):

    OFF_STUDY_MODEL = None

    objects = TestRegistrationManager()

    class Meta:
        app_label = 'testing'
