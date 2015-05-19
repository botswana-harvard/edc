import factory

from datetime import datetime

from edc.choices.common import IDENTITY_TYPE
from edc.core.bhp_variables.tests.factories import StudySiteFactory
from edc.subject.subject.tests.factories import BaseSubjectFactory

from ...models import TestConsent, TestConsentWithMixin


class BaseConsentBasicsFactory(BaseSubjectFactory):
    class Meta:
        abstract = True

    consent_reviewed = 'Yes'
    study_questions = 'Yes'
    assessment_score = 'Yes'
    consent_copy = 'Yes'


class BaseConsentFactory(BaseConsentBasicsFactory):
    class Meta:
        abstract = True

    study_site = factory.SubFactory(StudySiteFactory)
    consent_datetime = datetime.today()
    may_store_samples = 'Yes'
    is_incarcerated = 'No'


class BaseTestConsentFactory(BaseConsentFactory):
    class Meta:
        abstract = True

    user_provided_subject_identifier = None
    identity = factory.Sequence(lambda n: '{0}2{1}'.format(str(n).rjust(4, '0'), str(n).rjust(4, '0')))
    identity_type = factory.Iterator(IDENTITY_TYPE, getter=lambda c: c[0])
    confirm_identity = factory.Sequence(lambda n: '{0}2{1}'.format(str(n).rjust(4, '0'), str(n).rjust(4, '0')))
    first_name = factory.Sequence(lambda n: 'ERIK{0}'.format(n))
    initials = factory.Sequence(lambda n: 'E{0}W'.format(n))


class TestConsentFactory(BaseConsentFactory):
    class Meta:
        model = TestConsent


class TestConsentWithMixinFactory(BaseConsentFactory):
    class Meta:
        model = TestConsentWithMixin