import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import StudySite


class StudySiteFactory(BaseUuidModelFactory):
    FACTORY_FOR = StudySite

    site_code = factory.Sequence(lambda n: '1{0}'.format(n))
    site_name = factory.LazyAttribute(lambda o: 'Site_{0}'.format(o))
