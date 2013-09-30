from edc.core.bhp_base_model.tests.factories import BaseUuidModelFactory
from ...models import Configuration


class ConfigurationFactory(BaseUuidModelFactory):
    FACTORY_FOR = Configuration
