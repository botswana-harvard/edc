import factory
from datetime import datetime
from edc.core.bhp_base_model.tests.factories import BaseUuidModelFactory
from ...models import PreAppointmentContact
from .appointment_factory import AppointmentFactory


class PreAppointmentContactFactory(BaseUuidModelFactory):
    FACTORY_FOR = PreAppointmentContact

    appointment = factory.SubFactory(AppointmentFactory)
    contact_datetime = datetime.today()
    is_contacted = 'Yes'
    is_confirmed = True
