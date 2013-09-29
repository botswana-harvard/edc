import factory
from edc_core.bhp_base_model.tests.factories import BaseUuidModelFactory
from edc_core.bhp_visit.tests.factories import VisitDefinitionFactory
from edc_core.bhp_content_type_map.tests.factories import ContentTypeMapFactory
from ...models import Entry


class EntryFactory(BaseUuidModelFactory):
    FACTORY_FOR = Entry

    visit_definition = factory.SubFactory(VisitDefinitionFactory)
    content_type_map = factory.SubFactory(ContentTypeMapFactory)
    entry_order = factory.Sequence(lambda n: int(n) + 100)
