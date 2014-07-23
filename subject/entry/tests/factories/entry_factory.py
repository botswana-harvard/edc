import factory

from base.model.tests.factories import BaseUuidModelFactory
from core.bhp_content_type_map.tests.factories import ContentTypeMapFactory
from subject.visit_schedule.tests.factories import VisitDefinitionFactory

from ...models import Entry


class EntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = Entry

    visit_definition = factory.SubFactory(VisitDefinitionFactory)
    content_type_map = factory.SubFactory(ContentTypeMapFactory)
    entry_order = factory.Sequence(lambda n: int(n) + 100)
