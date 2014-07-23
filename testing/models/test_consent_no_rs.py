from django.db import models
from base.model.fields import IdentityTypeField
from core.crypto_fields.fields import EncryptedIdentityField
from subject.consent.models import BaseConsent
from subject.consent.managers import BaseConsentManager


class TestConsentNoRs(BaseConsent):

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

    def is_dispatchable_model(self):
        return False

    def get_user_provided_subject_identifier_attrname(self):
        """Returns the attribute name of the user provided subject_identifier."""
        return 'user_provided_subject_identifier'

    def get_subject_type(self):
        return 'subject'

    class Meta:
        app_label = 'testing'
