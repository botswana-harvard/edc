from datetime import date
import factory
from edc.base.model.tests.factories import BaseModelFactory
from ...models import UploadExportReceiptFile

class UploadExportReceiptFileFactory(BaseModelFactory):
    FACTORY_FOR = UploadExportReceiptFile
    
    file_name = factory.Sequence(lambda n: 'file_name{0}'.format(n))        
    receipt_datetime = date.today()