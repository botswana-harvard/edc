import factory
from edc.base.model.tests.factories import BaseUuidModelFactory
from apps.bcpp.bcpp_survey.models import Survey


class SurveyConfigurationFactory(BaseUuidModelFactory):
    FACTORY_FOR = Survey
