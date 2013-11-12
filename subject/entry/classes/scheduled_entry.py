from datetime import datetime, date

from django.db.models import get_model

from edc.subject.visit_tracking.settings import VISIT_REASON_NO_FOLLOW_UP_CHOICES

from ..models import Entry

from .base_scheduled_entry import BaseScheduledEntry


class ScheduledEntry(BaseScheduledEntry):

    def __init__(self, *args, **kwargs):
        self.meta_data_model = get_model('entry', 'ScheduledEntryMetaData')
        super(ScheduledEntry, self).__init__(*args, **kwargs)

    def set_filter_fieldname(self, filter_field_name=None):
        """Returns the field name for the foreign key that points to the visit model."""
        self._filter_fieldname = None
        if filter_field_name:
            self._filter_fieldname = filter_field_name
        else:
            if self.target_instance:
                # look for a field value that is a base of BaseVisitTracking, the target_model_base_cls
                for field in self.target_model._meta.fields:
                    if field.rel:
                        if issubclass(field.rel.to, self.target_model_base_cls):
                            self._filter_fieldname = field.name
                            break
            else:
                pass

    @property
    def meta_data_instance(self):
        return self._meta_data_instance

    @meta_data_instance.setter
    def meta_data_instance(self, meta_data_instance):
        if meta_data_instance:
            if not isinstance(meta_data_instance, self.meta_data_model):
                raise AttributeError('Attribute _meta_data_instance must be an instance of {0}. Got {1}'.format(self.meta_data_model, meta_data_instance.__class__))
        if not meta_data_instance:
            app_label = self.target_model._meta.app_label
            model_name = self.target_model._meta.model_name.lower()
            if Entry.objects.filter(visit_definition=self.appointment.visit_definition, app_label=app_label, model_name=model_name):
                entry = Entry.objects.get(
                    visit_definition=self.appointment.visit_definition,
                    app_label=app_label,
                    model_name=model_name)
                if self.meta_data_model.objects.filter(
                    appointment=self.appointment,
                    registered_subject=self.appointment.registered_subject,
                    entry=entry):
                    meta_data_instance = self.meta_data_model.objects.get(
                        appointment=self.appointment,
                        registered_subject=self.appointment.registered_subject,
                        entry=entry)
        self._meta_data_instance = meta_data_instance

    def show_scheduled_entries(self):
        if 'get_visit_reason_no_follow_up_choices' in dir(self.visit_instance):
            visit_reason_no_follow_up_choices = self.visit_instance.get_visit_reason_no_follow_up_choices()
        else:
            visit_reason_no_follow_up_choices = VISIT_REASON_NO_FOLLOW_UP_CHOICES
        show_scheduled_entries = self.visit_instance.reason.lower() not in [x.lower() for x in visit_reason_no_follow_up_choices.itervalues()]
        # possible conditions that override above
        # subject is at the off study visit (lost)
        if self.visit_instance.reason.lower() in self.visit_instance.get_off_study_reason():
            visit_date = date(self.visit_instance.report_datetime.year, self.visit_instance.report_datetime.month, self.visit_instance.report_datetime.day)
            if self.visit_instance.get_off_study_cls().objects.filter(registered_subject=self.registered_subject, offstudy_date=visit_date):
                # has an off study form completed on same day as visit
                off_study_instance = self.visit_instance.get_off_study_cls().objects.get(registered_subject=self.registered_subject, offstudy_date=visit_date)
                show_scheduled_entries = off_study_instance.show_scheduled_entries_on_off_study_date()
        return show_scheduled_entries

    def add_or_update_for_visit(self):
        """ Loops thru the list of entries configured for the visit_definition of this visit_instance
        and Adds entries to or updates existing entries in the meta_data."""
        for entry in Entry.objects.filter(visit_definition=self.appointment_zero.visit_definition):
            model = entry.get_model()
            model.entry_meta_data_manager.update_meta_data(self.visit_instance)

    def delete_for_visit(self):
        """Deletes meta data if visit is deleted."""
        # TODO: run this through the manager
        self.meta_data_model.objects.filter(appointment=self.visit_instance.appointment).delete()

    def update_status_from_instance(self, action, target_instance, filter_model_cls, comment=None):
        "Sets up then calls update meta_data using a user model instance."""
        self.target_model = target_instance.__class__
        self.target_instance = target_instance
        self.set_target_model(filter_model_cls)
        self.update_meta_data(action, None, comment)

    def update_status_from_rule(self, action, target_model, meta_data_instance, filter_instance, filter_attrname, comment=None):
        """Sets up then calls update meta_data given a meta_data instance id.

        Usually called from meta_data controller."""
        self.set_target_model(target_model)
        self.set_filter_instance(filter_instance)
        self.set_filter_fieldname(filter_attrname)
        self.meta_data_instance = meta_data_instance
        self.update_meta_data(action, self.visit_instance.report_datetime, comment)

    def get_next_entry_for(self, entry_order):
        next_meta_data_instance = None
        options = {
           'registered_subject_id': self.registered_subject.pk,
           'appointment_id': self.appointment.pk,
           #'entry__entry_category': entry_category,
            'entry_status': 'NEW',
            'entry__entry_order__gt': entry_order}
        if self.meta_data_model.objects.filter(**options):
            next_meta_data_instance = self.meta_data_model.objects.filter(**options)[0]
        return next_meta_data_instance

    def get_entries_for(self, entry_category, entry_status=None):
        """Returns a list of entry meta data instances for the given subject and zero instance appointment."""
        meta_data_instances = []
        if self.appointment:
            options = {
               'registered_subject_id': self.registered_subject.pk,
               'appointment_id': self.appointment_zero.pk,
               'entry__entry_category': entry_category,
               }
            if entry_status:
                options.update({'entry_status': entry_status})
            if not self.meta_data_model.objects.filter(**options).order_by('entry__entry_order'):
                # TODO: also if one meta data instance is missing, should figure it out (not just if ALL are missing)
                # refresh meta data for this appointment
                self.add_or_update_for_visit()
            meta_data_instances = self.meta_data_model.objects.filter(**options).order_by('entry__entry_order')
        return meta_data_instances
