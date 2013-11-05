from datetime import date

from django.db import models

from edc.base.model.models import BaseModel

class UploadSkipDays(BaseModel):

    skip_date = models.DateField(default=date.today(), unique=True)

    objects = models.Manager()
    
    def save(self, *args, **kwargs):
        super(UploadSkipDays, self).save(*args, **kwargs)
        
    def __unicode__(self):
        return unicode(self.skip_date)
        
    class Meta:
        app_label = 'import'
        ordering = ('-created', )
