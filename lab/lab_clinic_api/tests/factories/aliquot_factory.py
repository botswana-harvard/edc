import factory
from lis.specimen.lab_aliquot_list.tests.factories import BaseAliquotTypeFactory, BaseAliquotConditionFactory
from lis.specimen.lab_aliquot_list.models import AliquotType
from lis.specimen.lab_aliquot.tests.factories import BaseAliquotFactory
from ...models import Aliquot, AliquotCondition
from .receive_factory import ReceiveFactory


class AliquotConditionFactory(BaseAliquotConditionFactory):
    FACTORY_FOR = AliquotCondition


class AliquotTypeFactory(BaseAliquotTypeFactory):
    FACTORY_FOR = AliquotType
    dmis_reference = '1111'


class AliquotFactory(BaseAliquotFactory):
    FACTORY_FOR = Aliquot

    receive = factory.SubFactory(ReceiveFactory)
