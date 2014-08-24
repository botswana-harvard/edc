from datetime import datetime, timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from edc.subject.appointment.models import Appointment
from edc.choices.common import YES_NO_NA
from edc.core.crypto_fields.fields import EncryptedTextField
from edc.audit.audit_trail import AuditTrail
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.models import VisitDefinition
from edc.base.model.models import BaseModel


class TimePointCompletion(BaseModel):
    """ All completed appointments are noted in this form.
        Only authorized users can access this form.
        This form basically allows the user to definitely confirm
        that the appointment has been completed"""

    appointment = models.ForeignKey(Appointment, null=True)
    date_added = models.DateTimeField(
        verbose_name='Date added',
        default=datetime.today(),
        null=True)
    registered_subject = models.ForeignKey(RegisteredSubject,
        max_length=75)
    the_visit_code = models.ForeignKey(VisitDefinition,
        max_length=30,
        help_text=('the subjects current completed visit')
        )
    status = models.CharField(
        max_length=35,
        choices=(
            ('open', 'Open'),
            ('feedback', 'Feedback'),
            ('closed', 'Closed')),
        default='open',
        null=True,
        help_text='')
    comment = EncryptedTextField(
        max_length=500,
        null=True,
        blank=True)
    authorization = models.ForeignKey(User,
        verbose_name='Authorization (signature)',
        blank=True,
        null=True,
        editable=False
        )

    #adding fields for withdrawal of consent

    subject_withdrew = models.CharField(
        max_length=35,
        choices=YES_NO_NA,
        default='N/A',
        null=True,
        help_text='Use ONLY when subject has changed mind and wishes to withdraw consent')

    reasons_withdrawn = models.CharField(
        max_length=35,
        choices=(
            ('changed_mind', 'Subject changed mind'),
            ('N/A', 'Not applicable')),
        null=True,
        default='N/A',
        help_text='')

    date_withdrawn = models.DateTimeField(
        null=True,
        blank=True)

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return "for {0} at the {1} visit".format(self.registered_subject, self.the_visit_code)

    def get_report_datetime(self):
        return self.date_added

    def save(self, *args, **kwargs):
        self.confirm_appointment_status_before_setting_time_point_completion_to_closed()
        super(TimePointCompletion, self).save(*args, **kwargs)

    def confirm_appointment_status_before_setting_time_point_completion_to_closed(self):
        """closing off only appt that are either done/incomplete/cancelled ONLY"""
        if self.status == 'closed':
            from edc.subject.appointment.models import Appointment
            appointment = Appointment.objects.filter(registered_subject=self.registered_subject)
            if appointment[0].appt_status == 'new':
                raise ValidationError('You cannot close an appointment that has a NEW status')
            if appointment[0].appt_status == 'in_progress':
                raise ValidationError('You cannot close an appointment that is still in progress')
        elif self.status[0] == 'closed':
            if appointment[0].appt_status != ['done', 'incomplete', 'cancelled']:
                raise ValidationError('You cannot make a close off when the appointment status is not equal to DONE or INCOMPLETE or CANCELLED. Check appointment status first')

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
