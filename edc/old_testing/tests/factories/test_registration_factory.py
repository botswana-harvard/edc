import factory

from edc_testing.models import TestRegistration


class TestRegistrationFactory(factory.DjangoModelFactory):
    class Meta:
        model = TestRegistration
