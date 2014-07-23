from datetime import datetime
from base.model.tests.factories import BaseUuidModelFactory
from ...models import TestSubjectResultModel


class TestSubjectResultModelFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestSubjectResultModel

    result_datetime = datetime.today()
