from edc.base.model.models import BaseModel


class OutgoingTxSequence(BaseModel):

    def __unicode(self):
        return self.pk

    class Meta:
        app_label = 'sync'
