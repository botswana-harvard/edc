from .base_sequence import BaseSequence


class Sequence(BaseSequence):

    class Meta:
        app_label = 'identifier'
        db_table = 'bhp_identifier_sequence'
        ordering = ['id', ]
