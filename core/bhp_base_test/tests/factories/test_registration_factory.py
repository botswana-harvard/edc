from edc.core.bhp_registration.tests.factories import BaseRegistrationFactory
from ...models import TestRegistration


class TestRegistrationFactory(BaseRegistrationFactory):
    FACTORY_FOR = TestRegistration
