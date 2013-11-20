from edc.base.model.tests.factories import BaseModelFactory
from ...models import BaseReport

class BaseReportFactory(BaseModelFactory):
    
    FACTORY_FOR = BaseReport
    report_name = 'sample_report'
    report_url =  '/reports/'
    is_active = False