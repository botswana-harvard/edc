import factory
from lis.specimen.lab_receive.tests.factories import BaseReceiveFactory
from subject.registration.tests.factories import RegisteredSubjectFactory
from ...models import Receive


class ReceiveFactory(BaseReceiveFactory):
    FACTORY_FOR = Receive

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
