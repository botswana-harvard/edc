from datetime import datetime, timedelta
from django.db import models
from django.core.exceptions import ValidationError
from django.core.exceptions import ImproperlyConfigured
from django.contrib.auth.models import User
from django.core.urlresolvers import reverse

from edc.subject.appointment.choices import APPT_STATUS
from edc.subject.appointment.constants import DONE
from edc.core.crypto_fields.fields import EncryptedTextField
from edc.audit.audit_trail import AuditTrail
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.models import VisitDefinition
from edc.base.model.models import BaseModel


class QualityInspection(BaseModel):
    """ All completed appointments are noted in this form.
        Only authorized users can access this form.
        This form basically allows the user to definitely confirm
        that the appointment has been completed"""

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

    objects = models.Manager()

    history = AuditTrail()

    def __unicode__(self):
        return "for {0} at the {1} visit".format(self.registered_subject, self.the_visit_code)

    def save(self, *args, **kwargs):
        self.confirm_appointment_status_is_done_before_setting_quality_to_closed()
        super(QualityInspection, self).save(*args, **kwargs)

    def confirm_appointment_status_is_done_before_setting_quality_to_closed(self):
        """closing off only appt that are either done/incomplete/cancelled ONLY"""
        if self.status == 'closed':
            from edc.subject.appointment.models import Appointment
            appointment = Appointment.objects.get(registered_subject=self.registered_subject)
            if appointment.appt_status != ['done', 'incomplete', 'cancelled']:
                raise ValidationError('You cannot make a close off when the appointment status is not equal to DONE or INCOMPLETE or CANCELLED. Check appointment status first.')

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
        verbose_name = "Supervisor QA tool"
        verbose_name_plural = "Supervisor QA tool"
