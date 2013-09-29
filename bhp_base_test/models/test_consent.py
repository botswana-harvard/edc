from django.db import models
from edc_core.bhp_base_model.fields import IdentityTypeField
from edc_core.bhp_crypto.fields import EncryptedIdentityField
from edc_core.bhp_registration.models import RegisteredSubject
from edc_core.bhp_consent.models import BaseConsent
from edc_core.bhp_consent.managers import BaseConsentManager
from edc_core.bhp_appointment_helper.models import BaseAppointmentMixin
from .test_consent_history import TestConsentHistory


class BaseTestConsent(BaseConsent):
    """ Standard consent model.

    .. seealso:: :class:`BaseConsent` in :mod:`bhp_botswana.classes` """

    registered_subject = models.OneToOneField(RegisteredSubject, null=True)

    user_provided_subject_identifier = models.CharField(max_length=35, null=True)

    identity = EncryptedIdentityField(
        unique=True,
        null=True,
        blank=True,
        )

    identity_type = IdentityTypeField()

    confirm_identity = EncryptedIdentityField(
        unique=True,
        null=True,
        blank=True,
        )

    objects = BaseConsentManager()

    def get_consent_history_model(self):
        return TestConsentHistory

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
        app_label = 'bhp_base_test'


class TestConsentWithMixin(BaseAppointmentMixin, BaseTestConsent):

    def get_registration_datetime(self):
        return self.consent_datetime

    class Meta:
        app_label = 'bhp_base_test'
