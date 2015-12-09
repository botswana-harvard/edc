from django.db import models

from edc_consent.models import BaseConsent
from edc_consent.models.fields import ReviewFieldsMixin, IdentityFieldsMixin
from edc_base.model.models import BaseUuidModel
from edc.subject.appointment_helper.models import BaseAppointmentMixin
from edc.subject.registration.models import RegisteredSubject
from edc_consent.models.fields.sample_collection_fields_mixin import SampleCollectionFieldsMixin
from edc_consent.models.fields.personal_fields_mixin import PersonalFieldsMixin
from edc.core.bhp_variables.models.study_site import StudySite
from edc_consent.models.fields.vulnerability_fields_mixin import VulnerabilityFieldsMixin


class BaseTestConsent(BaseConsent, ReviewFieldsMixin, IdentityFieldsMixin, SampleCollectionFieldsMixin, PersonalFieldsMixin,
                      VulnerabilityFieldsMixin, BaseUuidModel):
    """ Standard consent model.

    .. seealso:: :class:`BaseConsent` in :mod:`bhp_botswana.classes` """

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    user_provided_subject_identifier = models.CharField(max_length=35, null=True)

    study_site = models.ForeignKey(StudySite)

    objects = models.Manager()

    def is_dispatchable_model(self):
        return False

    def get_user_provided_subject_identifier_attrname(self):
        """Returns the attribute name of the user provided subject_identifier."""
        return 'user_provided_subject_identifier'

    def get_subject_type(self):
        return 'test_subject_type'

    def get_registered_subject(self):
        return self.registered_subject

    class Meta:
        abstract = True


class TestConsent(BaseTestConsent):

    class Meta:
        app_label = 'testing'


class TestConsentWithMixin(BaseAppointmentMixin, BaseTestConsent):

    def get_registration_datetime(self):
        return self.consent_datetime

    class Meta:
        app_label = 'testing'
