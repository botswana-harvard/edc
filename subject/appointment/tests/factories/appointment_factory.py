import factory
from datetime import datetime
from subject.registration.tests.factories import RegisteredSubjectFactory
from subject.visit_schedule.tests.factories import VisitDefinitionFactory
from core.bhp_variables.tests.factories import StudySiteFactory
from base.model.tests.factories import BaseUuidModelFactory
from ...models import Appointment


class AppointmentFactory(BaseUuidModelFactory):
    FACTORY_FOR = Appointment

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    appt_datetime = datetime.today()
    best_appt_datetime = datetime.today()
    appt_close_datetime = datetime.today()
    study_site = factory.SubFactory(StudySiteFactory)
    visit_definition = factory.SubFactory(VisitDefinitionFactory)
    visit_instance = '0'
