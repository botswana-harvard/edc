import factory
from edc.subject.appointment.tests.factories import AppointmentFactory
from ...models import ScheduledEntryMetaData
from .base_entry_bucket_factory import BaseEntryMetaDataFactory
from .entry_factory import EntryFactory


class ScheduledEntryMetaDataFactory(BaseEntryMetaDataFactory):
    FACTORY_FOR = ScheduledEntryMetaData

    appointment = factory.SubFactory(AppointmentFactory)
    entry = factory.SubFactory(EntryFactory)
