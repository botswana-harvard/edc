from django.db import models
from edc.subject.registration.models import RegisteredSubject
from edc.subject.consent.models import BaseConsentedUuidModel
from .test_foreign_key import TestForeignKey
from .test_many_to_many import TestManyToMany
from .test_off_study_mixin import TestOffStudyMixin


class TestSubjectUuidModel(TestOffStudyMixin, BaseConsentedUuidModel):

    name = models.CharField(max_length=10)

    registered_subject = models.OneToOneField(RegisteredSubject)

    test_foreign_key = models.ForeignKey(TestForeignKey)

    test_many_to_many = models.ManyToManyField(TestManyToMany)

    objects = models.Manager()

    def get_subject_identifier(self):
        return self.registered_subject.subject_identifier

    def get_report_datetime(self):
        return self.created

    class Meta:
        app_label = 'testing'
