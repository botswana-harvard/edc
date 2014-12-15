from django.db import models

from lis.specimen.lab_aliquot.managers import AliquotManager
from lis.specimen.lab_aliquot.models import BaseAliquot

from .test_aliquot_condition import TestAliquotCondition
from .test_aliquot_type import TestAliquotType
from .test_receive import TestReceive
from .test_visit import TestVisit


class TestAliquot(BaseAliquot):

    receive = models.ForeignKey(TestReceive,
        editable=False)

    aliquot_type = models.ForeignKey(TestAliquotType,
        verbose_name="Aliquot Type",
        null=True)

    aliquot_condition = models.ForeignKey(TestAliquotCondition,
        verbose_name="Aliquot Condition",
        null=True,
        blank=True)

    objects = AliquotManager()

    def save(self, *args, **kwargs):
        self.subject_identifier = self.receive.registered_subject.subject_identifier
        super(TestAliquot, self).save(*args, **kwargs)

    @property
    def specimen_identifier(self):
        return self.aliquot_identifier[:-4]

    def get_visit_model(self):
        return TestVisit

    class Meta:
        app_label = 'testing'
        unique_together = (('receive', 'count'), )
        ordering = ('receive', 'count')
