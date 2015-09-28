from django.db import models
from django.conf import settings
from django.core.exceptions import ImproperlyConfigured

from edc.device.sync.models import BaseSyncUuidModel

from ..managers import IdentifierManager


class BaseIdentifierModel(BaseSyncUuidModel):
    """Store identifiers as allocated."""

    identifier = models.CharField(max_length=36, unique=True, editable=False)
    padding = models.IntegerField(default=4, editable=False)
    sequence_number = models.IntegerField()
    device_id = models.IntegerField(default=0)
    is_derived = models.BooleanField(default=False)
    sequence_app_label = models.CharField(max_length=50, editable=False, default='bhp_identifier')
    sequence_model_name = models.CharField(max_length=50, editable=False, default='sequence')

    def save(self, *args, **kwargs):
        try:
            self.device_id = settings.DEVICE_ID
        except AttributeError:
            raise ImproperlyConfigured('Settings attribute DEVICE_ID not found. Add DEVICE_ID '
                                       'to your settings.py where DEVICE_ID is a project wide '
                                       'unique integer.')
        if not self.id:
            if self.is_derived:
                self.sequence_number = 0
            else:
                Sequence = models.get_model(self.sequence_app_label, self.sequence_model_name)
                try:
                    sequence = Sequence.objects.using(
                        kwargs.get('using', None)).create(device_id=self.device_id)
                except AttributeError:
                    raise AttributeError('Unable to get model \'Sequence\' using Attributes '
                                         'sequence_app_label and sequence_model_name. Got {}, '
                                         '{}'.format(self.sequence_app_label,
                                                     self.sequence_model_name))
                self.sequence_number = sequence.pk
        if not self.identifier:
            raise AttributeError('IdentifierModel attribute \'identifier\' cannot be None. '
                                 'Set as a unique uuid or a unique formatted identifier.')
        super(BaseIdentifierModel, self).save(*args, **kwargs)

    @property
    def formatted_sequence(self):
        """Returns a padded sequence segment for the identifier"""
        if self.is_derived:
            return ''
        return str(self.sequence_number).rjust(self.padding, '0')

    objects = IdentifierManager()

    def natural_key(self):
        return (self.identifier, self.device_id, )

    def __unicode__(self):
        return self.identifier

    class Meta:
        abstract = True
