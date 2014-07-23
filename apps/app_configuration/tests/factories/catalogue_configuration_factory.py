import factory
from base.model.tests.factories import BaseUuidModelFactory
from subect.consent.models import ConsentCatalogue


class CatalogueConfigurationFactory(BaseUuidModelFactory):
    FACTORY_FOR = ConsentCatalogue
