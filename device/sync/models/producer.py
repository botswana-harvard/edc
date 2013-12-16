from django.db import models
from edc.base.model.models import BaseUuidModel


class Producer(BaseUuidModel):

    name = models.CharField(
        max_length=50,
        help_text='Usually hostname-database_name. e.g mpp83-bhp041_survey',
        unique=True,
        )

    settings_key = models.CharField(
        max_length=50,
        help_text='Key in settings.DATABASES, usually hostname of producer',
        unique=True,
        )

    url = models.CharField(
        max_length=64,
        )

    is_active = models.BooleanField(
        default=True
        )

    sync_datetime = models.DateTimeField(
        null=True
        )

    sync_status = models.CharField(
        max_length=250,
        default='-',
        null=True)
    
    json_limit = models.IntegerField(
        default=0)
    
    json_total_count = models.IntegerField(
        default=0
        )

    comment = models.TextField(
        max_length=50,
        null=True,
        blank=True)
    
    objects = models.Manager()


    def save(self, *args, **kwargs):
#         from django.conf import settings
#         print settings.DATABASES
#         producer_dict = {
#                 'ENGINE': 'django.db.backends.mysql',
#                 'TEST_MIRROR': None,
#                 'NAME': self.settings_key,
#                 'TEST_CHARSET': None,
#                 'TIME_ZONE': 'Africa/Gaborone',
#                 'TEST_COLLATION': None,
#                 'PORT': '3306',
#                 'HOST': self.url,
#                 'USER': self.settings_key,
#                 'TEST_NAME': None,
#                 'PASSWORD': 'cc3721b',
#                 'OPTIONS': {
#                     'init_command': 'SET storage_engine=INNODB'
#                 }
#             }
#         #if not settings.DATABASES.get(self.settings_key, None):
#         settings.DATABASES[self.settings_key] = producer_dict
#         print settings.DATABASES[self.settings_key]
        super(Producer, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sync'
        db_table = 'bhp_sync_producer'
        ordering = ['name']
        unique_together = (('settings_key', 'is_active'), )
