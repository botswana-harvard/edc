from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseModel
from edc_base.encrypted_fields import EncryptedCharField, EncryptedTextField, FirstnameField, LastnameField


class EncryptedTestModel(BaseModel):

    firstname = FirstnameField()

    lastname = LastnameField()

    char1 = EncryptedCharField()

    lastname2 = LastnameField()

    char2 = EncryptedCharField()

    text1 = EncryptedTextField()

    char3 = EncryptedCharField()

    text2 = EncryptedTextField()

    firstname2 = FirstnameField()

    text3 = EncryptedTextField()

    history = AuditTrail()

    def get_subject_identifier(self):
        return ''

    class Meta:
        app_label = 'testing'
