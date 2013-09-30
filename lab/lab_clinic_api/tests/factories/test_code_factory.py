from edc.lab.lab_test_code.tests.factories import BaseTestCodeFactory
from ...models import TestCode, TestCodeGroup


class TestCodeFactory(BaseTestCodeFactory):
    FACTORY_FOR = TestCode


class TestCodeGroupFactory(BaseTestCodeFactory):
    FACTORY_FOR = TestCodeGroup
