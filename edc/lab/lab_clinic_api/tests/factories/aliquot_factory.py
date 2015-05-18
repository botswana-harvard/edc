import factory

from lis.specimen.lab_aliquot.tests.factories import BaseAliquotFactory
from lis.specimen.lab_aliquot_list.tests.factories import BaseAliquotTypeFactory, BaseAliquotConditionFactory

from ...models import Aliquot, AliquotCondition, AliquotType

from .receive_factory import ReceiveFactory


class AliquotConditionFactory(BaseAliquotConditionFactory):
    FACTORY_FOR = AliquotCondition


class AliquotTypeFactory(BaseAliquotTypeFactory):
    FACTORY_FOR = AliquotType


class AliquotFactory(BaseAliquotFactory):
    FACTORY_FOR = Aliquot

    receive = factory.SubFactory(ReceiveFactory)
