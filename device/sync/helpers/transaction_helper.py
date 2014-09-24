from django.db.models import Q
from ..models import OutgoingTransaction, IncomingTransaction


class TransactionHelper(object):

    def has_incoming_for_producer(self, producer, using=None):
        if not using:
            using = 'default'
        return IncomingTransaction.objects.using(using).filter(producer=producer, is_consumed=False).exclude(Q(is_ignored=True) | Q(tx_name__contains='Audit')).exists()

    def has_incoming_for_model(self, models, using=None):
        """Checks if incoming transactions exist for the given model(s).
            models is a list of instance object names"""
        if not models:
            return False
        if not isinstance(models, (list, tuple)):
            models = [models]
        return IncomingTransaction.objects.using(using).filter(tx_name__in=models, is_consumed=False).exclude(is_ignored=True).exists()

    def has_outgoing(self, using=None):
        return OutgoingTransaction.objects.using(using).filter(is_consumed_server=False, is_consumed_middleman=False).exists()

    def has_outgoing_for_producer(self, producer, using=None):
        """Returns True if there are Outgoing Transactions where is_consumed_server=False,
        is_consumed_middleman=False."""
        if not using:
            using = 'default'
        return OutgoingTransaction.objects.using(using).filter(hostname_modified=producer, is_consumed_server=False, is_consumed_middleman=False).exclude(is_ignored=True).exists()


