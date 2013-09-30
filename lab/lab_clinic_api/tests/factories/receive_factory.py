import factory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from edc.lab.lab_receive.tests.factories import BaseReceiveFactory
from ...models import Receive


class ReceiveFactory(BaseReceiveFactory):
    FACTORY_FOR = Receive

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
