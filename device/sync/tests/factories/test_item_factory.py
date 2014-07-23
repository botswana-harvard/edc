from base.model.tests.factories import BaseUuidModelFactory
from device.sync.models import TestItem


class TestItemFactory(BaseUuidModelFactory):
    FACTORY_FOR = TestItem
