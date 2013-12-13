import logging

from datetime import datetime

from apps.bcpp.utils import Conf
from django.conf import settings
from django.core import serializers
from django.core.exceptions import ImproperlyConfigured
from django.db.models import get_model

from edc.base.model.models import BaseUuidModel

from ..classes import TransactionProducer

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class BaseSyncUuidModel(BaseUuidModel):

    """Base model for all UUID models and adds synchronization methods and signals. """

   #def is_serialized(self, serialize=True):
   #     if 'ALLOW_MODEL_SERIALIZATION' in dir(settings):
   #         if settings.ALLOW_MODEL_SERIALIZATION:
   #             return serialize
   #     return False

    def is_serialized(self, serialize=True):
        return Conf.get('ALLOW_MODEL_SERIALIZATION')

    def deserialize_prep(self):
        """Users may override to manipulate the incoming object before calling save()"""
        pass

    def _deserialize_post(self, incomming_transaction):
        """Default behaviour for all subclasses of this class is to serialize to outgoing transaction."""
        from ..models import OutgoingTransaction
        if not OutgoingTransaction.objects.filter(pk=incomming_transaction.id).exists():
                                                OutgoingTransaction.objects.create(
                                                    pk=incomming_transaction.id,
                                                    tx_name=incomming_transaction.tx_name,
                                                    tx_pk=incomming_transaction.tx_pk,
                                                    tx=incomming_transaction.tx,
                                                    timestamp=incomming_transaction.timestamp,
                                                    producer=incomming_transaction.producer,
                                                    action=incomming_transaction.action)
        self.deserialize_post()

    def deserialize_post(self):
        """Users may override to do app specific tasks after deserialization."""
        pass

    def deserialize_on_duplicate(self):
        """Users may override this to determine how to handle a duplicate error on deserialization.

        If you have a way to help decide if a duplicate should overwrite the existing record or not,
        evaluate your criteria here and return True or False. If False is returned to the deserializer,
        the object will not be saved and the transaction WILL be flagged as consumed WITHOUT error.
        """
        logger.info('method deserialize_on_duplicate is not defined, returning True')
        return True

    def deserialize_get_missing_fk(self, attrname):
        """Override to return a foreignkey object for 'attrname', if possible, using criteria in self, otherwise return None"""
        raise ImproperlyConfigured('Method deserialize_get_missing_fk() must be overridden on model class {0}'.format(self._meta.object_name))

    def save_to_inspector(self, fields):
        """Override in concrete class"""
        return False

    def delete(self, *args, **kwargs):
        """Creates a delete transaction on delete"""
        transaction_producer = TransactionProducer()
        if 'transaction_producer' in kwargs:
            transaction_producer = kwargs.get('transaction_producer')
            del kwargs['transaction_producer']

        if self.is_serialized() and not self._meta.proxy:
            OutgoingTransaction = get_model('sync', 'outgoingtransaction')
            json_obj = serializers.serialize("json", self.__class__.objects.filter(pk=self.pk), use_natural_keys=True)
            using = kwargs.get('using', 'default')
            OutgoingTransaction.objects.using(using).create(
                tx_name=self._meta.object_name,
                #app_label=self._meta.app_label,
                tx_pk=self.pk,
                tx=json_obj,
                timestamp=datetime.today().strftime('%Y%m%d%H%M%S%f'),
                producer=str(transaction_producer),
                action='D')
        super(BaseSyncUuidModel, self).delete(*args, **kwargs)

    class Meta:
        abstract = True
