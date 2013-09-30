from edc.subject.registration.tests.factories import BaseRegistrationFactory
from ...models import TestRegistration


class TestRegistrationFactory(BaseRegistrationFactory):
    FACTORY_FOR = TestRegistration
