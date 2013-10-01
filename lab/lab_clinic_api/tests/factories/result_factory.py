import factory
from lis.specimen.lab_result.tests.factories import BaseResultFactory
from ...models import Result
from .order_factory import OrderFactory


class ResultFactory(BaseResultFactory):
    FACTORY_FOR = Result

    order = factory.SubFactory(OrderFactory)
