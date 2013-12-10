import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.subject.appointment.models import Configuration


class AppointmentConfigurationFactory(BaseUuidModelFactory):
    FACTORY_FOR = Configuration
