from datetime import date, timedelta

from django.db import models

from edc.base.model.models import BaseModel
from apps.bcpp.choices import COMMUNITIES

class UploadSkipDays(BaseModel):

    skip_date = models.DateField(default=date.today(), unique=True)
    
    identifier = models.CharField(max_length=50, choices=COMMUNITIES)

    objects = models.Manager()
    
    def save(self, *args, **kwargs):
        if self.today_upload_exists():
            raise TypeError('An upload file for \'{0}\' already exists. So cannot create it as a skip date'.format(self.skip_date))
        #A skip day is only valid there was an upload the previous day or if the previous day was also a skip day.
        if not self.previous_day_file_uploaded() and not self.skip_previous_day():
            raise TypeError('Missing Upload file from the previous day. Previous day is not set as a SKIP date. Therefore \'{0}\' is not a valid skip date.'.format(self.skip_date))
        super(UploadSkipDays, self).save(*args, **kwargs)
     
    def previous_day_file_uploaded(self):
        from .upload_transaction_file import UploadTransactionFile
        previous = self.skip_date - timedelta(1)
        if UploadTransactionFile.objects.filter(file_date=previous, identifier=self.identifier).exists():
            return True
        return False
    
    def today_upload_exists(self):
        from .upload_transaction_file import UploadTransactionFile
        if UploadTransactionFile.objects.filter(file_date=self.skip_date, identifier=self.identifier).exists():
            return True
        return False
    
    def skip_previous_day(self):
        yesterday = self.skip_date - timedelta(1)
        if self.__class__.objects.filter(skip_date=yesterday, identifier=self.identifier).exists():
            return True
        return False
            
    def __unicode__(self):
        return unicode(self.skip_date)
        
    class Meta:
        app_label = 'import'
        ordering = ('-created', )
