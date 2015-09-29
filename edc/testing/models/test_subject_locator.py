from django.db import models

from edc_base.model.models.base_uuid_model import BaseUuidModel
from edc.subject.locator.models import BaseLocator

from .test_visit import TestVisit


class TestSubjectLocator(BaseLocator, BaseUuidModel):

    test_visit = models.OneToOneField(TestVisit)

    def get_subject_identifier(self):
        return self.test_visit.get_subject_identifier()

    class Meta:
        app_label = 'testing'
