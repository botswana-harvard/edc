import factory
from datetime import datetime
from edc_core.bhp_base_model.tests.factories import BaseUuidModelFactory
from edc_core.bhp_appointment.tests.factories import AppointmentFactory


class BaseVisitTrackingFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    appointment = factory.SubFactory(AppointmentFactory)
    report_datetime = datetime.today()
    reason = 'scheduled'
    reason_missed = None
    info_source = 'subject'
