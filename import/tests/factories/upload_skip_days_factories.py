from datetime import date
import factory
from base.model.tests.factories import BaseModelFactory
from ...models import UploadSkipDays

class UploadSkipDaysFactory(BaseModelFactory):
    FACTORY_FOR = UploadSkipDays
    
    skip_date = date.today()   
    identifier = factory.Sequence(lambda n: 'identifier{0}'.format(n))