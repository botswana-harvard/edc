import factory

from base.model.tests.factories import BaseUuidModelFactory
from lab.lab_clinic_api.tests.factories import PanelFactory
from subject.visit_schedule.tests.factories import VisitDefinitionFactory

from ...models import LabEntry


class LabEntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = LabEntry

    visit_definition = factory.SubFactory(VisitDefinitionFactory)

    entry_order = factory.Sequence(lambda n: int(n) + 100)

    panel = factory.SubFactory(PanelFactory)
