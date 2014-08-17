import socket
from datetime import datetime
from django.conf import settings
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import StudySpecific


class StudySpecificFactory(BaseUuidModelFactory):
    FACTORY_FOR = StudySpecific

    protocol_number = settings.PROJECT_NUMBER
    protocol_code = settings.PROJECT_IDENTIFIER_PREFIX
    protocol_title = settings.PROJECT_TITLE
    research_title = settings.PROJECT_TITLE
    study_start_datetime = datetime(datetime.today().year - 6, 1, 1)
    minimum_age_of_consent = 16
    maximum_age_of_consent = 64
    gender_of_consent = 'MF'
    subject_identifier_prefix = settings.PROJECT_IDENTIFIER_PREFIX
    hostname_prefix = socket.gethostname()
    device_id = 0
