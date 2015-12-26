import factory
import socket

from datetime import datetime

from ...models import StudySpecific


class StudySpecificFactory(factory.DjangoModelFactory):
    class Meta:
        model = StudySpecific

    study_start_datetime = datetime(datetime.today().year - 6, 1, 1)
    minimum_age_of_consent = 16
    maximum_age_of_consent = 64
    gender_of_consent = 'MF'
    hostname_prefix = socket.gethostname()
    device_id = 0
