import factory
from edc.lab.lab_result_item.tests.factories import BaseResultItemFactory
from ...models import ResultItem
from .result_factory import ResultFactory
from .test_code_factory import TestCodeFactory


class ResultItemFactory(BaseResultItemFactory):
    FACTORY_FOR = ResultItem

    result = factory.SubFactory(ResultFactory)
    test_code = factory.SubFactory(TestCodeFactory)
