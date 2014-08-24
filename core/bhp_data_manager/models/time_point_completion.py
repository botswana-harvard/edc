from datetime import datetime

from django.core.exceptions import ValidationError
from django.core.urlresolvers import reverse
from django.db import models

from edc.audit.audit_trail import AuditTrail
from edc.base.model.models import BaseModel
from edc.choices.common import YES_NO_NA
from edc.core.crypto_fields.fields import EncryptedTextField
from edc.subject.appointment.models import Appointment


class TimePointCompletion(BaseModel):
    """ All completed appointments are noted in this form.

    Only authorized users can access this form. This form allows
    the user to definitely confirm that the appointment has
    been completed"""

    appointment = models.ForeignKey(Appointment)

    close_datetime = models.DateTimeField(
        verbose_name='Date and time appointment "closed" for edit.',
        default=datetime.today())

    status = models.CharField(
        max_length=15,
        choices=(
            ('open', 'Open'),
            ('feedback', 'Feedback'),
            ('closed', 'Closed')),
        default='open',
        help_text='')

    comment = EncryptedTextField(
        max_length=500,
        null=True,
        blank=True)

    subject_withdrew = models.CharField(
        verbose_name='Did the participant withdraw consent?',
        max_length=15,
        choices=YES_NO_NA,
        default='N/A',
        null=True,
        help_text='Use ONLY when subject has changed mind and wishes to withdraw consent')

    reasons_withdrawn = models.CharField(
        verbose_name='Reason participant withdrew consent',
        max_length=35,
        choices=(
            ('changed_mind', 'Subject changed mind'),
            ('N/A', 'Not applicable')),
        null=True,
        default='N/A',
        help_text='')

    withdraw_datetime = models.DateTimeField(
        verbose_name='Date and time participant withdrew consent',
        null=True,
        blank=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return "for {0} at the {1} visit".format(self.registered_subject, self.the_visit_code)

    def get_report_datetime(self):
        return self.date_added

    def save(self, *args, **kwargs):
        self.validate_status()
        super(TimePointCompletion, self).save(*args, **kwargs)

    def validate_status(self, exception_cls=None):
        """Closing off only appt that are either done/incomplete/cancelled ONLY."""
        exception_cls = exception_cls or ValidationError
        if self.status == 'closed' and self.appointment.appt_status in ['new', 'in_progress']:
            raise exception_cls('You cannot close an appointment that has a {0} status'.format(self.appointment.appt_status.upper()))

    def dashboard(self):
        ret = None
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                url = reverse('subject_dashboard_url',
                              kwargs={'dashboard_type': self.registered_subject.subject_type.lower(),
                                      'dashboard_model': 'registered_subject',
                                      'dashboard_id': self.registered_subject.pk,
                                      'show': 'appointments'})
                ret = """<a href="{url}" />dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    class Meta:
        app_label = "bhp_data_manager"
        verbose_name = "Time Point Completion tool"
        verbose_name_plural = "Time Point Completion tool"
