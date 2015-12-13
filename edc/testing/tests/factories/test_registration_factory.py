import factory

from edc.testing.models import TestRegistration


class TestRegistrationFactory(factory.DjangoModelFactory):
    class Meta:
        model = TestRegistration
