from edc.core.bhp_base_model.tests.factories import BaseListModelFactory
from ...models import DeathCauseCategory


class DeathCauseCategoryFactory(BaseListModelFactory):
    FACTORY_FOR = DeathCauseCategory
