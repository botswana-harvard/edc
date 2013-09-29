import factory
from edc_core.bhp_base_model.tests.factories import BaseUuidModelFactory
from edc_core.bhp_content_type_map.tests.factories import ContentTypeMapFactory
from ...models import VisitDefinition

starting_seq_num = 1000


class VisitDefinitionFactory(BaseUuidModelFactory):
    FACTORY_FOR = VisitDefinition
    code = factory.Sequence(lambda n: 'CODE{0}'.format(n))
    title = factory.Sequence(lambda n: 'TITLE{0}'.format(n))
    visit_tracking_content_type_map = factory.SubFactory(ContentTypeMapFactory)
