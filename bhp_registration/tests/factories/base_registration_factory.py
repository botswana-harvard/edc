import factory
from datetime import datetime
from edc_core.bhp_base_model.tests.factories import BaseUuidModelFactory
from .registered_subject_factory import RegisteredSubjectFactory


class BaseRegistrationFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    registration_datetime = datetime.today()
