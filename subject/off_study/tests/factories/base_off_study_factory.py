import factory
from datetime import date
from base.model.tests.factories import BaseUuidModelFactory
from subject.registration.tests.factories import RegisteredSubjectFactory


class BaseOffStudyFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    offstudy_date = date.today()
    reason = 'reason'
