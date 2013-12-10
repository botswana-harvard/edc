import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.subect.consent.models import ConsentCatalogue


class CatalogueConfigurationFactory(BaseUuidModelFactory):
    FACTORY_FOR = ConsentCatalogue
