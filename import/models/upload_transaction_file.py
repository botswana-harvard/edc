from datetime import date, timedelta

from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

from edc.base.model.models import BaseModel
from edc.device.sync.classes import DeserializeFromTransaction
from edc.device.sync.models import IncomingTransaction
from .upload_skip_days import UploadSkipDays


class UploadTransactionFile(BaseModel):

    transaction_file = models.FileField(upload_to=settings.MEDIA_ROOT)

    file_name = models.CharField(max_length=50, null=True, editable=False, unique=True)

    file_date = models.DateField(null=True, editable=False, unique=True)
    
    identifier = models.CharField(max_length=50, null=True) 
    
    consume = models.BooleanField(default=True)

    total = models.IntegerField(editable=False, default=0)

    consumed = models.IntegerField(editable=False, default=0)

    not_consumed = models.IntegerField(editable=False, default=0, help_text='duplicates')

    producer = models.TextField(max_length=1000, null=True, editable=False, help_text='List of producers detected from the file.')

    objects = models.Manager()
    
    def save(self, *args, **kwargs):
        if not self.id:
            self.file_name = self.transaction_file.name.replace('\\', '/').split('/')[-1]
            date_string = self.file_name.split('_')[2].split('.')[0][:8]
            self.file_date = date(int(date_string[:4]),int(date_string[4:6]), int(date_string[6:8]))
            self.identifier = self.file_name.split('_')[1]
            self.check_for_transactions()
            if self.consume:
                self.consume_transactions()
        super(UploadTransactionFile, self).save(*args, **kwargs)

    def check_for_transactions(self, transaction_file=None, exception_cls=None):
        transaction_file = transaction_file or self.transaction_file
        transaction_file.open()
        exception_cls = exception_cls or ValidationError
        deserializer = DeserializeFromTransaction()
        if not deserializer.deserialize_json_file(transaction_file):
            raise exception_cls('File does not contain any transactions. Got {0}'.format(transaction_file.name))

    def consume_transactions(self):
        if self.today_set_as_skip_day():
            raise TypeError('Date \'{0}\' is already added to the skip table. So cannot upload on a date set to be skipped.'.format(self.file_date))
        #Can only upload if there exists an upload from the previous day, or a valid skip day exists in its preence.
        if self.file_already_uploaded():
            raise TypeError('File covering date of \'{0}\', is already uploaded.'.format(self.file_name))
        if not self.is_previous_day_file_uploaded() and not self.skip_previous_day():
            raise TypeError('Missing Upload file from the previous day. Previous day is not set as a SKIP date.'.format())
        deserializer = DeserializeFromTransaction()
        index = 0
        self.transaction_file.open()
        producer_list = []
        for index, outgoing in enumerate(deserializer.deserialize_json_file(self.transaction_file)):
            if not IncomingTransaction.objects.filter(pk=outgoing.get('pk')).exists():
                if outgoing.get('fields'):
                    self.consumed += 1
                    IncomingTransaction.objects.create(
                        pk=outgoing.get('pk'),
                        tx_name=outgoing.get('fields').get('tx_name'),
                        tx_pk=outgoing.get('fields').get('tx_pk'),
                        tx=outgoing.get('fields').get('tx'),
                        timestamp=outgoing.get('fields').get('timestamp'),
                        producer=outgoing.get('fields').get('producer'),
                        action=outgoing.get('fields').get('action'))
                    if outgoing.get('fields').get('producer') not in producer_list:
                        producer_list.append(outgoing.get('fields').get('producer'))
            else:
                self.not_consumed += 1
        self.total = index
        producer_list.sort()
        self.producer = ','.join(producer_list)
        
    def file_already_uploaded(self):
        if self.__class__.objects.filter(file_date=self.file_date, identifier=self.identifier).exists():
            return True
        return False
    
    def is_previous_day_file_uploaded(self):
        yesterday = self.file_date - timedelta(1)
        if self.__class__.objects.filter(file_date=yesterday, identifier=self.identifier).exists():
            return True
        return False
    
    def skip_previous_day(self):
        yesterday = self.file_date - timedelta(1)
        if UploadSkipDays.objects.filter(skip_date=yesterday, identifier=self.identifier).exists():
            return True
        return False
    
    def today_set_as_skip_day(self):
        if UploadSkipDays.objects.filter(skip_date=self.file_date, identifier=self.identifier).exists():
            return True
        return False
    
    def __unicode__(self):
        return unicode(self.file_name)
    
    class Meta:
        app_label = 'import'
        ordering = ('-created', )
