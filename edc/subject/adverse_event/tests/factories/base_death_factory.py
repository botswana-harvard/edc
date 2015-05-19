import factory
from datetime import date
from edc.base.model.tests.factories import BaseUuidModelFactory, BaseListModelFactory
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from ...models import DeathMedicalResponsibility, DeathCauseCategory, DeathCauseInfo


class DeathMedicalResponsibilityFactory(BaseListModelFactory):
    FACTORY_FOR = DeathMedicalResponsibility


class DeathCauseCategoryFactory(BaseListModelFactory):
    FACTORY_FOR = DeathCauseCategory


class DeathCauseInfoFactory(BaseListModelFactory):
    FACTORY_FOR = DeathCauseInfo


class BaseDeathFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    registered_subject = factory.SubFactory(RegisteredSubjectFactory)
    death_date = date.today()
    death_medical_responsibility = factory.SubFactory(DeathMedicalResponsibilityFactory)
    death_cause_info = factory.SubFactory(DeathCauseInfoFactory)
    death_cause_category = factory.SubFactory(DeathCauseCategoryFactory)
    participant_hospitalized = 'No'