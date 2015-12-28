from django.db import models
from edc_registration.models import RegisteredSubject
from .test_foreign_key import TestForeignKey
from .test_m2m import TestM2m
from edc_offstudy.models import OffStudyMixin


class TestSubjectUuidModel(OffStudyMixin, models.Model):

    name = models.CharField(max_length=10)

    registered_subject = models.OneToOneField(RegisteredSubject)

    test_foreign_key = models.ForeignKey(TestForeignKey)

    test_m2m = models.ManyToManyField(TestM2m)

    objects = models.Manager()

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_report_datetime(self):
        return self.created

    class Meta:
        app_label = 'testing'
