from django.db import models

from edc_base.encrypted_fields import IdentityField
from edc_base.model.fields import IdentityTypeField
from edc_consent.models import BaseConsent


class TestConsentNoRs(BaseConsent):

    user_provided_subject_identifier = models.CharField(max_length=35, null=True)

    identity = IdentityField(
        unique=True,
        null=True,
        blank=True,
    )

    identity_type = IdentityTypeField()

    confirm_identity = IdentityField(
        unique=True,
        null=True,
        blank=True,
    )

    def is_dispatchable_model(self):
        return False

    def get_user_provided_subject_identifier_attrname(self):
        """Returns the attribute name of the user provided subject_identifier."""
        return 'user_provided_subject_identifier'

    def get_subject_type(self):
        return 'subject'

    class Meta:
        app_label = 'testing'
