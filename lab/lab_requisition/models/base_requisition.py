from django.core.serializers.base import SerializationError
from django.core.urlresolvers import reverse
from django.db import models

from lab.lab_clinic_api.models import TestCode

from .base_base_requisition import BaseBaseRequisition


class BaseRequisition (BaseBaseRequisition):

    # populate this one based on the selected panel at the dashboard
    test_code = models.ManyToManyField(TestCode,
        verbose_name='Additional tests',
        null=True,
        blank=True,
        )

    subject_identifier = models.CharField(
        max_length=25,
        null=True,
        editable=False)

    def save(self, *args, **kwargs):
        self.subject_identifier = self.get_visit().get_subject_identifier()
        super(BaseRequisition, self).save(*args, **kwargs)

    def dispatch_container_lookup(self, using=None):
        return None

    def natural_key(self):
        return (self.requisition_identifier,)

    def get_subject_identifier(self):
        return self.get_visit().subject_identifier

    def get_visit(self):
        raise TypeError('method \'get_visit()\' in BaseRequisition must be overidden')

    def dashboard(self):
        url = reverse('subject_dashboard_url',
                      kwargs={'dashboard_type': self.get_visit().appointment.registered_subject.subject_type.lower(),
                              'dashboard_model': 'appointment',
                              'dashboard_id': self.get_visit().appointment.pk,
                              'show': 'appointments'})
        return """<a href="{url}" />dashboard</a>""".format(url=url)
    dashboard.allow_tags = True

    class Meta:
        abstract = True
