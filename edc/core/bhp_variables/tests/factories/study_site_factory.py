import factory

from edc.base.model.tests.factories import BaseUuidModelFactory

from edc.core.bhp_variables.models import StudySite


class StudySiteFactory(BaseUuidModelFactory):

    class Meta:
        model = StudySite

    site_code = factory.Sequence(lambda n: '1{0}'.format(n))
    site_name = factory.LazyAttribute(lambda o: 'Site_{0}'.format(o))
