import factory
from ...models import AliquotType
from .base_aliquot_type_factory import BaseAliquotTypeFactory


class AliquotTypeFactory(BaseAliquotTypeFactory):
    FACTORY_FOR = AliquotType

    dmis_reference = factory.Sequence(lambda n: n)
