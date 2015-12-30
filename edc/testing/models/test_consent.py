from django.db import models

from edc_registration.models import RegisteredSubject
from edc_appointment.models import AppointmentMixin
from edc_base.model.models import BaseUuidModel
from edc_consent.models import BaseConsent
from edc_consent.models.fields import ReviewFieldsMixin, IdentityFieldsMixin
from edc_consent.models.fields.personal_fields_mixin import PersonalFieldsMixin
from edc_consent.models.fields.sample_collection_fields_mixin import SampleCollectionFieldsMixin
from edc_consent.models.fields.vulnerability_fields_mixin import VulnerabilityFieldsMixin


class BaseTestConsent(BaseConsent, ReviewFieldsMixin, IdentityFieldsMixin,
                      SampleCollectionFieldsMixin, PersonalFieldsMixin,
                      VulnerabilityFieldsMixin, BaseUuidModel):

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    user_provided_subject_identifier = models.CharField(max_length=35, null=True)

    objects = models.Manager()

    def is_dispatchable_model(self):
        return False

    def get_subject_type(self):
        return 'test_subject_type'

    def get_registered_subject(self):
        return self.registered_subject

    class Meta:
        abstract = True


class TestConsent(BaseTestConsent):

    class Meta:
        app_label = 'testing'


class TestConsentWithMixin(AppointmentMixin, BaseTestConsent):

    def get_registration_datetime(self):
        return self.consent_datetime

    class Meta:
        app_label = 'testing'
