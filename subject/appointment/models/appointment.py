from django.db import models
from django.core.urlresolvers import reverse
from django.core.validators import RegexValidator
from django.core.exceptions import ValidationError

from edc.audit.audit_trail import AuditTrail
from edc.core.bhp_variables.models import StudySite
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_schedule.classes import WindowPeriod
from edc.subject.visit_schedule.models import VisitDefinition
from edc.core.bhp_data_manager.models import QualityInspection

from ..managers import AppointmentManager
from ..choices import APPT_TYPE
from ..constants import DONE

from .base_appointment import BaseAppointment

from edc.core.bhp_data_manager.models import QualityInspection


class Appointment(BaseAppointment):
    """Tracks appointments for a registered subject's visit.

        Only one appointment per subject visit_definition+visit_instance.
        Attribute 'visit_instance' should be populated by the system.
    """
    registered_subject = models.ForeignKey(RegisteredSubject, related_name='+')

    best_appt_datetime = models.DateTimeField(null=True, editable=False)

    appt_close_datetime = models.DateTimeField(null=True, editable=False)

    study_site = models.ForeignKey(
        StudySite,
        null=True,
        blank=False)

    visit_definition = models.ForeignKey(
        VisitDefinition,
        related_name='+',
        verbose_name=("Visit"),
        help_text=("For tracking within the window period of a visit, use the decimal convention. "
                   "Format is NNNN.N. e.g 1000.0, 1000.1, 1000.2, etc)"))

    visit_instance = models.CharField(
        max_length=1,
        verbose_name=("Instance"),
        validators=[RegexValidator(r'[0-9]', 'Must be a number from 0-9')],
        default='0',
        null=True,
        blank=True,
        db_index=True,
        help_text=("A decimal to represent an additional report to be included with the original "
                   "visit report. (NNNN.0)"))
    dashboard_type = models.CharField(
        max_length=25,
        editable=False,
        null=True,
        blank=True,
        db_index=True,
        help_text='hold dashboard_type variable, set by dashboard')

    appt_type = models.CharField(
        verbose_name='Appointment type',
        choices=APPT_TYPE,
        default='clinic',
        max_length=20,
        help_text='Default for subject may be edited in admin under section bhp_subject. See Subject Configuration.')

    history = AuditTrail()

    quality_inspection_status = models.ForeignKey(QualityInspection)

    objects = AppointmentManager()

    def natural_key(self):
        """Returns a natural key."""
        return (self.visit_instance, ) + self.visit_definition.natural_key() + self.registered_subject.natural_key()
    natural_key.dependencies = ['registration.registeredsubject', 'bhp_visit.visitdefinition']

    def validate_appt_datetime(self, exception_cls=None):
        """Returns the appt_datetime, possibly adjusted, and the best_appt_datetime, the calculated ideal timepoint datetime.

        .. note:: best_appt_datetime is not editable by the user. If 'None', will raise an exception."""
        from edc.subject.appointment_helper.classes import AppointmentDateHelper
        # for tests
        if not exception_cls:
            exception_cls = ValidationError
        appointment_date_helper = AppointmentDateHelper()
        if not self.id:
            appt_datetime = appointment_date_helper.get_best_datetime(self.appt_datetime, self.study_site)
            best_appt_datetime = self.appt_datetime
        else:
            if not self.best_appt_datetime:
                # did you update best_appt_datetime for existing instances since the migration?
                raise exception_cls('Appointment instance attribute \'best_appt_datetime\' cannot be null on change.')
            appt_datetime = appointment_date_helper.change_datetime(self.best_appt_datetime, self.appt_datetime, self.study_site, self.visit_definition)
            best_appt_datetime = self.best_appt_datetime
        return appt_datetime, best_appt_datetime

    def validate_visit_instance(self, using=None, exception_cls=None):
        """Confirms a 0 instance appointment exists before allowing a continuation appt and keep a sequence."""
        if not exception_cls:
            exception_cls = ValidationError
        if not isinstance(self.visit_instance, basestring):
            raise exception_cls('Expected \'visit_instance\' to be of type basestring')
        if self.visit_instance != '0':
            if not Appointment.objects.using(using).filter(
                    registered_subject=self.registered_subject,
                    visit_definition=self.visit_definition,
                    visit_instance='0').exclude(pk=self.pk).exists():
                raise exception_cls('Cannot create continuation appointment for visit %s. Cannot find the original appointment (visit instance equal to 0).' % (self.visit_definition,))
            if int(self.visit_instance) - 1 != 0:
                if not Appointment.objects.using(using).filter(
                        registered_subject=self.registered_subject,
                        visit_definition=self.visit_definition,
                        visit_instance=str(int(self.visit_instance) - 1)).exists():
                    raise exception_cls('Cannot create continuation appointment for visit {0}. '
                                        'Expected next visit instance to be {1}. Got {2}'.format(self.visit_definition,
                                                                                                 str(int(self.visit_instance) - 1),
                                                                                                 self.visit_instance))

    def check_window_period(self, exception_cls=None):
        """Is this used?"""
        if not exception_cls:
            exception_cls = ValidationError
        if self.id:
            window_period = WindowPeriod()
            if not window_period.check_datetime(self.visit_definition, self.appt_datetime, self.best_appt_datetime):
                raise exception_cls(window_period.error_message)

    def save(self, *args, **kwargs):
        """Django save method"""
        from edc.subject.appointment_helper.classes import AppointmentHelper
        using = kwargs.get('using')
        self.appt_datetime, self.best_appt_datetime = self.validate_appt_datetime()
        self.check_window_period()
        self.validate_visit_instance(using=using)
        self.close_off_appointment()
        self.prevent_further_edit_to_appointment_when_status_is_done()
        AppointmentHelper().check_appt_status(self, using)
        super(Appointment, self).save(*args, **kwargs)

    def raw_save(self, *args, **kwargs):
        """Optional save to bypass stuff going on in the default save method."""
        super(Appointment, self).save(*args, **kwargs)

    def close_off_appointment(self):
        """checks if the appointment status is done"""
        if self.appt_status == 'done':
            """confirms if the Quality Inspection form is auto filled, if not, create it (auto fill)"""
            def confirm_quality_inspection_exists():
                try:
                    return QualityInspection.objects.filter(registered_subject=self.registered_subject, the_visit_code=self.visit_definition.code)
                except QualityInspection.DoesNotExist:
                    return False
            if not confirm_quality_inspection_exists():
                QualityInspection.objects.create(registered_subject=self.registered_subject, the_visit_code=self.visit_definition)

    def prevent_further_edit_to_appointment_when_status_is_done(self):
        """this is to prevent any further edits to the appointment once its confirmed
        that both the appt_status and quality_status are set to done and closed respectively"""
        appointment = Appointment.objects.filter(registered_subject=self.registered_subject, visit_definition=self.visit_definition)
        if appointment:
            if not appointment.count() > 1:
                quality_closed = models.get_model('bhp_data_manager', 'QualityInspection').objects.filter(registered_subject=self.registered_subject, the_visit_code=self.visit_definition)
                if quality_closed:
                    if appointment[0].appt_status == 'done' and quality_closed[0].status == 'closed':
                        if appointment.appt_status in ['new', 'in_progress', 'incomplete', 'cancelled']:
                            raise ValidationError('This appointment is closed off and no further edits can be made')

    def __unicode__(self):
        """Django."""
        return "{0} {1} for {2}.{3}".format(self.registered_subject.subject_identifier, self.registered_subject.subject_type, self.visit_definition.code, self.visit_instance)

    def dashboard(self):
        """Returns a hyperink for the Admin page."""
        ret = None
        if self.registered_subject:
            if self.registered_subject.subject_identifier:
                url = reverse('subject_dashboard_url',
                              kwargs={'dashboard_type': self.registered_subject.subject_type.lower(),
                                      'dashboard_model': 'appointment',
                                      'dashboard_id': self.pk,
                                      'show': 'appointments'})
                ret = """<a href="{url}" />dashboard</a>""".format(url=url)
        return ret
    dashboard.allow_tags = True

    def get_subject_identifier(self):
        """Returns the subject identifier."""
        return self.registered_subject.subject_identifier

    def get_registered_subject(self):
        """Returns the registered subject."""
        return self.registered_subject

    def get_report_datetime(self):
        """Returns the appointment datetime as the report_datetime."""
        return self.appt_datetime

    def allow_missing_forms(self):
        """ This method will look for the existence of a model record that allows it to close visit as done even though not all forms filled eg participation model in BCPP """
        from django.db.models import get_model
        from edc.subject.entry.models import Entry
        from .base_participation_model import BaseParticipationModel
        scheduled_entries = Entry.objects.all()
        for entry in scheduled_entries:
            model_class = get_model(entry.app_label, entry.model_name)
            if issubclass(model_class, BaseParticipationModel):
                if model_class.objects.filter(subject_visit__appointment=self).exists():
                    model_instance = model_class.objects.get(subject_visit__appointment=self)
                    if 'allow_missing_forms' in dir(model_instance):
                        return model_instance.allow_missing_forms()
        return False

    @property
    def complete(self):
        """Returns True if the appointment status is DONE."""
        return self.appt_status == DONE

    class Meta:
        """Django model Meta."""
        app_label = 'appointment'
        db_table = 'bhp_appointment_appointment'
        unique_together = (('registered_subject', 'visit_definition', 'visit_instance'),)
        ordering = ['registered_subject', 'appt_datetime', ]
