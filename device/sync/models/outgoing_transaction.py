from datetime import datetime

from django.db import models

from .base_transaction import BaseTransaction

from .outgoing_tx_sequence import OutgoingTxSequence


class OutgoingTransaction(BaseTransaction):

    """ transactions produced locally to be consumed/sent to a queue or consumer """
    is_consumed_middleman = models.BooleanField(
        default=False,
        db_index=True,
        )

    is_consumed_server = models.BooleanField(
        default=False,
        db_index=True,
        )

    tx_sequence = models.IntegerField(unique=True, null=True)

    objects = models.Manager()

    def save(self, *args, **kwargs):
        if not self.id:
            self.tx_sequence = OutgoingTxSequence.objects.create().id
        if self.is_consumed_server and not self.consumed_datetime:
                self.consumed_datetime = datetime.today()
        super(OutgoingTransaction, self).save(*args, **kwargs)

    class Meta:
        app_label = 'sync'
        db_table = 'bhp_sync_outgoingtransaction'
        ordering = ['timestamp']
