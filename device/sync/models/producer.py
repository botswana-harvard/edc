from django.db import models
from django.conf import settings

from edc.core.crypto_fields.fields import EncryptedCharField
from edc.base.model.models import BaseUuidModel


class Producer(BaseUuidModel):

    name = models.CharField(
        max_length=50,
        help_text='Usually hostname-database_name. e.g mpp83-bhp041_survey',
        unique=True)

    settings_key = models.CharField(
        max_length=50,
        help_text='Key in settings.DATABASES, usually hostname of producer',
        unique=True)

    url = models.CharField(max_length=64)

    producer_ip = EncryptedCharField(
        verbose_name="Producer IP address.",
        null=True,
        db_index=True,
        help_text=("provide the IP address of the producer."))

    db_user = EncryptedCharField(
        verbose_name="Database username.",
        default='root',
        null=True,
        db_index=True,
        help_text=("provide the database name of the producer."))

    db_user_name = EncryptedCharField(
        verbose_name="Database name.",
        null=True,
        db_index=True,
        help_text=("provide the database name of the producer."))

    port = EncryptedCharField(
        verbose_name="Database port.",
        default='',
        blank=True,
        null=True,
        help_text=("provide the database name of the producer."))

    db_password = EncryptedCharField(
        verbose_name="Database password.",
        null=True,
        db_index=True,
        help_text=("provide the password to database on the producer."))

    is_active = models.BooleanField(
        default=True)

    sync_datetime = models.DateTimeField(
        null=True)

    sync_status = models.CharField(
        max_length=250,
        default='-',
        null=True)

    json_limit = models.IntegerField(
        default=0)

    json_total_count = models.IntegerField(
        default=0)

    comment = models.TextField(
        max_length=50,
        null=True,
        blank=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        settings.DATABASES[self.settings_key] = {
            'ENGINE': 'django.db.backends.mysql',
            'OPTIONS': {
                'init_command': 'SET storage_engine=INNODB',
            },
            'NAME': self.db_user_name,
            'USER': self.db_user,
            'PASSWORD': self.db_password,
            'HOST': self.producer_ip,
            'PORT': self.port,
        }
        super(Producer, self).save(*args, **kwargs)

    def __unicode__(self):
        return self.name

    class Meta:
        app_label = 'sync'
        db_table = 'bhp_sync_producer'
        ordering = ['name']
        unique_together = (('settings_key', 'is_active'), )
