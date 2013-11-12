from django.core.exceptions import ImproperlyConfigured
from django.db import models

from edc.core.bhp_common.utils import convert_from_camel
from edc.subject.entry.models import ScheduledEntryMetaData, Entry
from edc.subject.lab_entry.models import ScheduledLabEntryMetaData, LabEntry
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.visit_tracking.models import BaseVisitTracking


class BaseMetaDataManager(models.Manager):

    """Creates, updates or deletes meta data that tracks the entry status of models for a given visit."""
    meta_data_model = None
    skip_create_visit_reasons = ['missed', 'death', 'lost']  # list of visit reasons where meta data should not be created
    may_delete_entry_status = ['NEW', 'NOT_REQUIRED']

    def __init__(self, visit_model, visit_attr_name=None):
        self.visit_model = visit_model
        self.visit_attr_name = visit_attr_name or convert_from_camel(self.visit_model._meta.object_name)
        super(BaseMetaDataManager, self).__init__()

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, instance_or_visit_instance):
        """Sets the model instance referred to by the meta data directly or from the visit instance."""
        self._instance = None
        if isinstance(instance_or_visit_instance, self.model):
            self._instance = instance_or_visit_instance
            self.visit_instance = getattr(self.instance, self.visit_attr_name)
        elif isinstance(instance_or_visit_instance, BaseVisitTracking):
            if super(EntryMetaDataManager, self).filter(**{self.visit_attr_name: instance_or_visit_instance}):
                self._instance = super(EntryMetaDataManager, self).get(**{self.visit_attr_name: instance_or_visit_instance})
            self.visit_instance = instance_or_visit_instance
        # reset meta data instance
        self._meta_data_instance = None
        # reset status
        self.status = None

    @property
    def visit_model(self):
        """Returns the visit model that is a foreign key on the model referred to by the meta data."""
        return self._visit_model

    @visit_model.setter
    def visit_model(self, visit_model):
        if not visit_model:
            raise AttributeError('MetaDataManager expects \'visit_model\'. Got None.')
        self._visit_model = visit_model

    @property
    def meta_data_instance(self):
        """Returns the meta data instance using the meta data's "model" instance.

        Will be created if DoesNotExist."""
        if not self._meta_data_instance:
            try:
                self._meta_data_instance = self.meta_data_model.objects.get(
                    appointment=self.visit_instance.appointment,
                    entry__app_label=self.model._meta.app_label,
                    entry__model_name=self.model._meta.object_name.lower(),
                    )
            except self.meta_data_model.DoesNotExist:
                self._meta_data_instance = self.create_meta_data()
        return self._meta_data_instance

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, change_type):
        """Figures out the the current status of the user model instance, KEYED or NEW (not keyed).

        Insert, Update and Delete (I, U, D) come from the signal.
        """
        if not change_type:
            change_type = 'Exists'
            if not self.instance:
                change_type = 'DoesNotExist'
        change_types = {'DoesNotExist': 'NEW', 'Exists': 'KEYED', 'I': 'KEYED', 'U': 'KEYED', 'D': 'NEW'}
        if change_type not in change_types:
            raise ValueError('Change type must be any of {0}. Got {1}'.format(change_types.keys(), change_type))
        self._status = change_types.get(change_type)

    def create_meta_data(self):
        raise ImproperlyConfigured('Override to create a new meta data instance')

    def update_meta_data(self, instance, change_type, using=None):
        raise ImproperlyConfigured('Unable to update meta data.')

    def delete_meta_data(self):
        if not self.instance and self.status in self.may_delete_entry_status:
            self.meta_data_instance.delete()

    def run_rule_groups(self):
        """Runs rule groups for this visit instance."""
        site_rule_groups.update_for_visit_definition(self.visit_instance)


class EntryMetaDataManager(BaseMetaDataManager):

    meta_data_model = ScheduledEntryMetaData

    def create_meta_data(self):
        """Creates a meta_data instance for the model at the time point (appointment) for the given registered_subject.

        might NOT be created based on visit reason."""
        if self.visit_instance.reason not in self.skip_create_visit_reasons:
            entry = Entry.objects.get(
                app_label=self.model._meta.app_label,
                model_name=self.model._meta.object_name.lower(),
                visit_definition=self.visit_instance.appointment.visit_definition
                )
            return self.meta_data_model.objects.create(
                appointment=self.visit_instance.appointment,
                registered_subject=self.visit_instance.appointment.registered_subject,
                due_datetime=entry.visit_definition.get_upper_window_datetime(self.visit_instance.report_datetime),
                entry=entry,
                entry_status=self.status
                )
        return None

    def update_meta_data(self, model_or_visit_instance, change_type=None, using=None):
        """Updates the meta_data's instance.

        Called by the signal on post_save and pre_delete"""
        self.instance = model_or_visit_instance
        if self.meta_data_instance:
            if change_type == 'D' or not self.instance:
                self.meta_data_instance.report_datetime = None
            else:
                self.meta_data_instance.report_datetime = self.instance.report_datetime
            self.status = change_type
            self.meta_data_instance.entry_status = self.status
            self.meta_data_instance.save()
        self.run_rule_groups()


class ReqisitionMetaDataStatusManager(BaseMetaDataManager):

    meta_data_model = ScheduledLabEntryMetaData

    # TODO: since this manages meta data around a single model, the requisition model, entry__app_label and entry__model_name do
    #       not apply. need to know the entry__panel to update or create
#     def create_meta_data(self):
#         """Creates a meta_data instance for the model at the time point (appointment) for the given registered_subject.
# 
#         might NOT be created based on visit reason."""
#         if self.visit_instance.reason not in self.skip_create_visit_reasons:
#             entry = LabEntry.objects.get(
#                 app_label=self.model._meta.app_label,
#                 model_name=self.model._meta.object_name.lower(),
#                 visit_definition=self.visit_instance.appointment.visit_definition
#                 )
#             return self.meta_data_model.objects.create(
#                 appointment=self.visit_instance.appointment,
#                 registered_subject=self.visit_instance.appointment.registered_subject,
#                 due_datetime=entry.visit_definition.get_upper_window_datetime(self.visit_instance.report_datetime),
#                 entry=entry,
#                 entry_status=self.status
#                 )
#         return None
# 
#     def update_meta_data(self, model_or_visit_instance, change_type=None, using=None):
#         """Updates the meta_data's instance.
# 
#         Called by the signal on post_save and pre_delete"""
#         self.instance = model_or_visit_instance
#         if self.meta_data_instance:
#             if change_type == 'D' or not self.instance:
#                 self.meta_data_instance.report_datetime = None
#             else:
#                 self.meta_data_instance.report_datetime = self.instance.report_datetime
#             self.status = change_type
#             self.meta_data_instance.entry_status = self.status
#             self.meta_data_instance.save()
#         self.run_rule_groups()
