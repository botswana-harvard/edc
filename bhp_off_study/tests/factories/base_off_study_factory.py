import factory
from datetime import date
from edc_core.bhp_base_model.tests.factories import BaseUuidModelFactory
from edc_core.bhp_registration.tests.factories import RegisteredSubjectFactory


class BaseOffStudyFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    offstudy_date = date.today()
    reason = 'reason'
