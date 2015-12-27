from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model

from ..exceptions import ProducerError

from .base_using import BaseUsing


class BaseProducer(BaseUsing):

    def __init__(self, using_source, using_destination):
        super(BaseProducer, self).__init__(using_source, using_destination)
        self._producer = None

    @property
    def producer(self):
        """Sets the instance of the current producer based on
        the ORM `using` parameter for the destination.

        .. note:: The producer must always exist on the source."""
        if not self._producer:
            Producer = get_model('edc_sync', 'Producer')
            try:
                self._producer = Producer.objects.using(
                    self.using_source).get(settings_key=self.using_destination, is_active=True)
            except Producer.DoesNotExist:
                raise ProducerError(
                    'Dispatcher cannot find a producer with settings key \'{0}\' '
                    'on the source {1}.'.format(self.using_destination, self.using_source))
            # check the producers DATABASES key exists
            # TODO: what if producer is "me", e.g settings key is 'default'
            if not self.using_destination == 'default':
                settings_key = self._producer.settings_key
                if not [dbkey for dbkey in settings.DATABASES.iteritems() if dbkey[0] == settings_key]:
                    raise ImproperlyConfigured(
                        'Dispatcher expects settings attribute DATABASES to have a NAME '
                        'key to the \'producer\'. Got name=\'{0}\', settings_key=\'{1}\'.'.format(
                            self._producer.name, self._producer.settings_key))
        return self._producer
