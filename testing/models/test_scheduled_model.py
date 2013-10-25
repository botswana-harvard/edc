from datetime import datetime

from django.db import models

from edc.base.model.models import BaseUuidModel

from .test_visit import TestVisit


class TestScheduledModel(BaseUuidModel):

    test_visit = models.OneToOneField(TestVisit)

    report_datetime = models.DateTimeField(default=datetime.today())

    f1 = models.CharField(max_length=10, null=True)

    f2 = models.CharField(max_length=10, null=True)

    f3 = models.CharField(max_length=10, null=True)

    f4 = models.CharField(max_length=10, null=True)

    def get_subject_identifier(self):
        return self.test_visit.get_subject_identifier()

    class Meta:
        app_label = 'testing'
