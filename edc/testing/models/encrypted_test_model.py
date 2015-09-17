from edc_audit.audit_trail import AuditTrail
from edc.base.model.models import BaseModel
from edc.core.crypto_fields.fields import EncryptedCharField, EncryptedTextField, EncryptedFirstnameField, EncryptedLastnameField


class EncryptedTestModel(BaseModel):

    firstname = EncryptedFirstnameField()

    lastname = EncryptedLastnameField()

    char1 = EncryptedCharField()

    lastname2 = EncryptedLastnameField()

    char2 = EncryptedCharField()

    text1 = EncryptedTextField()

    char3 = EncryptedCharField()

    text2 = EncryptedTextField()

    firstname2 = EncryptedFirstnameField()

    text3 = EncryptedTextField()

    history = AuditTrail(show_in_admin=True)

    def get_subject_identifier(self):
        return ''

    class Meta:
        app_label = 'testing'
