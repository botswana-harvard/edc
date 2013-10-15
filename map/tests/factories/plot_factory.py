import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import Plot


class PlotFactory(BaseUuidModelFactory):
    FACTORY_FOR = Plot

    gps_target_lon = 25.745569 
    gps_target_lat = -25.032927