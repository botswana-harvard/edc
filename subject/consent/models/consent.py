from edc.base.model.fields import IdentityTypeField
from edc.core.crypto_fields.fields import EncryptedIdentityField
from ..models import BaseConsent


class Consent(BaseConsent):

    """ Standard consent model.

    .. seealso:: :class:`BaseConsent` in :mod:`local.bw.classes` """

    identity = EncryptedIdentityField(
        unique=True,
        null=True,
        blank=True,
        )

    identity_type = IdentityTypeField()

    def __unicode__(self):
        return unicode(self.subject_identifier)

    class Meta:
        abstract = True
