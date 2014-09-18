import socket
import logging
from django.conf import settings
from django.db.models import get_model


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class TransactionProducer(object):

    def __init__(self, **kwargs):

        if kwargs.get('hostname'):
            self.value = kwargs.get('hostname')
        else:
            # add on the DB name so that if on the same host still get a unique name
            self.value = '%s-%s' % (socket.gethostname().lower(), settings.DATABASES['default']['NAME'].lower())

    def __get__(self, instance, owner):
        return self.value

    def __str__(self):
        return self.value