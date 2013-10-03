import logging
from datetime import datetime, timedelta
from django.db.models import get_model
from django.core.serializers.base import DeserializationError
from .deserialize_from_transaction import DeserializeFromTransaction
from ..exceptions import TransactionConsumerError


logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class Consumer(object):

    def __init__(self):
        from edc.device.dispatch.classes import SignalManager
        self.signal_manager = SignalManager()

    def consume(self, using=None, lock_name=None, **kwargs):
        """Consumes ALL incoming transactions on \'using\' in order by ('producer', 'timestamp')."""
        if not using:
            using = None
        IncomingTransaction = get_model('sync', 'IncomingTransaction')
        check_hostname = kwargs.get('check_hostname', True)
        deserialize_from_transaction = DeserializeFromTransaction()
        tot = IncomingTransaction.objects.using(using).filter(is_consumed=False).count()
        for n, incoming_transaction in enumerate(IncomingTransaction.objects.using(using).filter(is_consumed=False, is_ignored=False).order_by('producer', 'timestamp')):
            action = ''
            print '{0} / {1} {2} {3}'.format(n + 1, tot, incoming_transaction.producer, incoming_transaction.tx_name)
            print '    tx_pk=\'{0}\''.format(incoming_transaction.tx_pk)
            action = 'failed'
            try:
                self._disconnect_signals(incoming_transaction.tx_name.lower())
                if deserialize_from_transaction.deserialize(incoming_transaction, using, check_hostname=check_hostname):
                    action = 'saved'
                self._reconnect_signals()
                print '    {0}'.format(action)
            except DeserializationError as e:
                self._reconnect_signals()
                print '    {0} {1}'.format(action, e)
                pass  # raise DeserializationError(e)

    def _disconnect_signals(self, obj):
        self.signal_manager.disconnect(obj)
        self.disconnect_signals()

    def disconnect_signals(self):
        """Disconnects app specific signals if overriden."""
        pass

    def _reconnect_signals(self):
        self.signal_manager.reconnect()
        self.reconnect_signals()
        self.signal_manager.reconnect()

    def reconnect_signals(self):
        """Reconnects app specific signals if overriden."""
        pass
    
    def get_consume_feedback(self):
        from ..models import IncomingTransaction
        today = datetime.now()
        margin = timedelta(microseconds=999)
        consumed_today = IncomingTransaction.objects.filter(created__range=(today - margin, today + margin), is_consumed=True)
        not_consumed_today = IncomingTransaction.objects.filter(created__range=(today - margin, today + margin), is_consumed=False)
        not_consumed_not_ignored_today = not_consumed_today.filter(is_ignored=False)
        message = '\'{0}\' transactions where consumed today, \n \'{1}\' transactions failed to consume today, \n \'{2}\' of those that failed to consume have been set as ignored.'.format(
                    consumed_today.count(),not_consumed_today.count(),not_consumed_not_ignored_today.count())
        return message
        
    def fetch_outgoing(self, using_source, using_destination=None):
        """Fetches all OutgoingTransactions not consumed from a source and saves them locally (default).

            Args:
                using_source: DATABASE key for the database with the OutgoingTransactions
                using_destination: DATABASE key for the database receiving the IncoingTransactions. (default=default)"""
        if not using_destination:
            using_destination = 'default'
        if using_source == using_destination:
            raise TransactionConsumerError('Cannot fetch outgoing transactions from myself')
        OutgoingTransaction = get_model('sync', 'OutgoingTransaction')
        IncomingTransaction = get_model('sync', 'IncomingTransaction')
        for outgoing_transaction in OutgoingTransaction.objects.using(using_source).filter(is_consumed=False):
            new_incoming_transaction = IncomingTransaction()
            # copy outgoing attr into new incoming
            for field in OutgoingTransaction._meta.fields:
                if field.attname not in ['id', 'is_consumed']:
                    setattr(new_incoming_transaction, field.attname, getattr(outgoing_transaction, field.attname))
            new_incoming_transaction.is_consumed = False
            # save incoming on destination
            new_incoming_transaction.save(using=using_destination)
            outgoing_transaction.is_consumed = True
            # update outgoing on source
            outgoing_transaction.save(using=using_source)
