import factory
from base.model.tests.factories import BaseUuidModelFactory
from core.bhp_variables.models import StudySpecific


class VariblesConfigurationFactory(BaseUuidModelFactory):
    FACTORY_FOR = StudySpecific
