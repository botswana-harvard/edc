from django.core.exceptions import ValidationError
from django.db import models
from django.conf import settings

from edc.base.model.models import BaseModel
from edc.device.sync.classes import DeserializeFromTransaction
from edc.device.sync.models import IncomingTransaction


class UploadTransactionFile(BaseModel):

    transaction_file = models.FileField(upload_to=settings.MEDIA_ROOT)

    file_name = models.CharField(max_length=50, null=True, editable=False)

    consume = models.BooleanField(default=True)

    total = models.IntegerField(editable=False, default=0)

    consumed = models.IntegerField(editable=False, default=0)

    not_consumed = models.IntegerField(editable=False, default=0, help_text='duplicates')

    producer = models.TextField(maxlength=1000, null=True, editable=False, help_text='List of producers detected from the file.')

    def save(self, *args, **kwargs):
        if not self.id:
            self.file_name = self.transaction_file.name.replace('\\', '/').split('/')[-1]
            if not self.check_for_transactions():
                raise ValidationError('File does not contain any transactions. Got {0}'.format(self.file_name))
            if self.consume:
                self.consume_transactions()
        super(UploadTransactionFile, self).save(*args, **kwargs)

    def check_for_transactions(self):
        deserializer = DeserializeFromTransaction()
        return deserializer.deserialize_json_file(self.transaction_file)

    def consume_transactions(self):
        deserializer = DeserializeFromTransaction()
        index = 0
        self.transaction_file.open()
        producer_list = []
        for index, outgoing in enumerate(deserializer.deserialize_json_file(self.transaction_file)):
            if not IncomingTransaction.objects.filter(pk=outgoing.get('pk')).exists():
                if outgoing.get('fields'):
                    self.consumed += 1
                    IncomingTransaction.objects.create(
                        pk=outgoing.get('pk'),
                        tx_name=outgoing.get('fields').get('tx_name'),
                        tx_pk=outgoing.get('fields').get('tx_pk'),
                        tx=outgoing.get('fields').get('tx'),
                        timestamp=outgoing.get('fields').get('timestamp'),
                        producer=outgoing.get('fields').get('producer'),
                        action=outgoing.get('fields').get('action'))
                    if outgoing.get('fields').get('producer') not in self.producer:
                        producer_list.append(outgoing.get('fields').get('producer'))
            else:
                self.not_consumed += 1
        self.total = index
        producer_list.sort()
        self.producer = ','.join(producer_list)

    class Meta:
        app_label = 'import'
        ordering = ('-created', )
