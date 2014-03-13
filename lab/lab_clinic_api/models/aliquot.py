from django.db import models
from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse

from lis.specimen.lab_aliquot.models import BaseAliquot

from .aliquot_condition import AliquotCondition
from .aliquot_type import AliquotType
from .receive import Receive


class Aliquot(BaseAliquot):
    """Stores aliquot information and is the central model in the RAORR relational model."""

    primary_aliquot = models.ForeignKey('self',
        null=True,
        related_name='primary',
        editable=False)

    source_aliquot = models.ForeignKey('self',
        null=True,
        related_name='source',
        editable=False,
        help_text='Aliquot from which this aliquot was created, Leave blank if this is the primary tube')

    receive = models.ForeignKey(Receive,
        editable=False)

    aliquot_type = models.ForeignKey(AliquotType,
        verbose_name="Aliquot Type",
        null=True)

    aliquot_count = models.IntegerField(default=1)

    aliquot_condition = models.ForeignKey(AliquotCondition,
        verbose_name="Aliquot Condition",
        null=True,
        blank=True)

    subject_identifier = models.CharField(
        max_length=50,
        null=True,
        editable=False,
        help_text="non-user helper field to simplify search and filtering")

    receive_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False,
        help_text="non-user helper field to simplify search and filter")

    #is_labeled = models.BooleanField()

    objects = models.Manager()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.receive.registered_subject.subject_identifier
        self.receive_identifier = self.receive.receive_identifier
        if self.source_aliquot and not self.primary_aliquot:
            raise ValidationError('Primary aliquot may not be None')
        super(Aliquot, self).save(*args, **kwargs)

    def get_subject_identifier(self):
        return self.subject_identifier

    def drawn(self):
        return self.receive.drawn_datetime

    def barcode_value(self):
        return self.aliquot_identifier

    def to_receive(self):
        return '<a href="/admin/lab_clinic_api/receive/?q={receive_identifier}">{receive_identifier}</a>'.format(receive_identifier=self.receive.receive_identifier)
    to_receive.allow_tags = True

#     def requisition(self):
#         if self.receive:
#             requisition = self.receive.requisition
#             url = reverse('admin:{0}_{1}_change_list')
#         return '<a href="{0}?{requisition}={1}">process</a>'.format(url, self.pk, requisition='')
#     requisition.allow_tags = True

    def process(self):
        url = reverse('admin:lab_clinic_api_processing_add')
        return '<a href="{0}?aliquot={1}">process</a>'.format(url, self.pk)
    process.allow_tags = True

    def __unicode__(self):
        return self.aliquot_identifier

    class Meta:
        app_label = 'lab_clinic_api'
        unique_together = (('receive', 'aliquot_count'), )
        ordering = ('receive', 'aliquot_count')
