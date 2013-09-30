from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Configuration


class ConfigurationFactory(BaseUuidModelFactory):
    FACTORY_FOR = Configuration
