import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import StudySite


class StudySiteFactory(BaseUuidModelFactory):
    FACTORY_FOR = StudySite

    site_code = factory.Sequence(lambda n: '{0}'.format(n))
    site_name = factory.LazyAttribute(lambda o: 'Site {0}'.format(o.site_code))
