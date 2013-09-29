from django.conf import settings
from django.core.exceptions import ObjectDoesNotExist
from ...bhp_registration.models import RegisteredSubject
from ..sms_error_codes import (SEARCH_SUBJECT_ID_SMS_FORMAT_ERR,
                                     SUBJECT_IDENTIFIER_NOT_FOUND, SUBJECT_IDENTIFIER_FOUND)
from .sms import Sms


class ServerSmsController(Sms):
    """Expects sms text with format:

    prefix token first_name dob omang e.g
    041 490fefcbad8ac3f23fd28af3d196eb0a2fa0f PANTANOWITZ 1945-01-09 987123343
    """
    def __explode_message(self, text):
        data = []
        pieces = text.split(self.DELIMETER)
        data['prefix'] = pieces[0]
        data['token'] = pieces[1]
        data['first_name'] = pieces[2]
        data['dob'] = pieces[3]
        data['omang'] = pieces[4]
        return data

    def __validate_get_identifier_sms(self, text):
        return False

    """Prepare text message to be sent to client.
    Prefix - A keyword to assist kannel route the sms to appropriate service (view)
    """
    def prepare_reply(self):
        reply = ""
        if settings.SMS_PREFIX:
            reply = "{0} {1} {2}".format(settings.SMS_PREFIX, self.result['token'], self.result['subject_identifier'])
        else:
            raise ValueError("SMS_PREFIX is not set on the settings file")
        return reply

    def process_message(self, msg):
        if settings.IS_SERVER:
            if self.__validate_get_identifier_sms(msg.text):
                data = self.__explode_message(msg.text)
                dob = data.get('dob')
                omang = data.get('omang')
                first_name = data.get('first_name')
                token = data.get('token')
                try:
                    subject = RegisteredSubject.objects.get(
                        dob=dob, first_name=first_name, identity=omang
                        )
                    self.result['subject_identifier'] = subject.subject_idenfier
                    self.result['omang'] = subject.omang
                    self.result['dob'] = subject.dob
                    self.result['first_name'] = subject.first_name
                    self.result['token'] = token
                    self.result['error_code'] = SUBJECT_IDENTIFIER_FOUND
                except ObjectDoesNotExist:
                    self.result['error_code'] = SUBJECT_IDENTIFIER_NOT_FOUND
            else:
                self.result['error_code'] = SEARCH_SUBJECT_ID_SMS_FORMAT_ERR
        else:
            raise ValueError("IS_SERVER should set to True on the settings file if we are on server")
