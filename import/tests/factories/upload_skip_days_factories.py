from datetime import date
import factory
from edc.base.model.tests.factories import BaseModelFactory
from ...models import UploadSkipDays

class UploadSkipDaysFactory(BaseModelFactory):
    FACTORY_FOR = UploadSkipDays

    skip_date = date.today()
    skip_until_date = None
    identifier = factory.Sequence(lambda n: 'identifier{0}'.format(n))