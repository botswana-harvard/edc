from django.core.exceptions import ImproperlyConfigured
from django.db import models

from edc.core.bhp_common.utils import convert_from_camel
from edc.subject.entry.models import ScheduledEntryMetaData, Entry
from edc.subject.lab_entry.models import ScheduledLabEntryBucket
from edc.subject.rule_groups.classes import site_rule_groups


class BaseMetaDataManager(models.Manager):

    """Creates, updates or deletes meta data that tracks the entry status of models for a given visit.

    Works with a signals.

    Does not reference rule groups."""
    meta_data_model = None
    skip_create_visit_reasons = ['missed', 'death', 'lost']
    may_delete_entry_status = ['NEW', 'NOT_REQUIRED']

    def __init__(self, visit_model=None, visit_attr_name=None):
        self._instance = None
        if not visit_model:
            raise ImproperlyConfigured('MetaDataManager expects \'visit_model\'. Got None.')
        self._visit_model = visit_model
        if not visit_attr_name:
            self._visit_attr_name = convert_from_camel(visit_model._meta.object_name)
        super(BaseMetaDataManager, self).__init__()

    def get_visit_model(self):
        """Returns the visit model that is a foreign key on the model referred to by the meta data."""
        return self._visit_model

    def get_visit_attr_name(self):
        return self._visit_attr_name

    def get_visit_instance(self, instance):
        return getattr(instance, self.get_visit_attr_name())

    def get_meta_data_model(self):
        if not self.meta_data_model:
            raise AttributeError('Attribute meta_data_model may not be None.')
        return self.meta_data_model

    def set_instance(self, instance=None, visit_instance=None):
        """Sets the model instance referred to by the meta data directly or with a given visit instance."""
        if visit_instance:
            if super(EntryMetaDataManager, self).filter(**{self.get_visit_attr_name(): visit_instance}):
                self._instance = super(EntryMetaDataManager, self).get(**{self.get_visit_attr_name(): visit_instance})
        elif instance:
            self._instance = instance
        else:
            raise AttributeError('Expected either \'instance\' or \'visit_instance\'. Got neither.')
        if self._instance:
            if not isinstance(self._instance, self.model):
                raise TypeError('Model instance must be an instance of {0}. Got {1}'.format(self.model, self._instance.__class__))

    def get_instance(self):
        return self._instance

    def get_appointment(self, instance):
        return self.get_visit_instance(instance).appointment

    def set_meta_data_instance(self, instance):
        """Sets the meta data instance, (not the model instance referred to by the meta data).

        Will be created if DoesNotExist."""
        try:
            self._meta_data_instance = self.get_meta_data_model().objects.get(
                appointment=self.get_appointment(instance),
                entry__app_label=instance._meta.app_label,
                entry__model_name=instance._meta.object_name.lower(),
                )
        except self.get_meta_data_model().DoesNotExist:
            self._meta_data_instance = self.create_meta_data(instance)

    def get_meta_data_instance(self):
        """Returns the meta data instance, may be None so you need to test the value first."""
        return self._meta_data_instance

    def get_change_type(self):
        if not self.get_instance():
            return 'DoesNotExist'
        return 'Exists'

    def get_status(self, change_type=None):
        """Figures out the the current status of the user model instance, KEYED or NEW (not keyed).

        Insert, Update and Delete (I, U, D) come from the signal.
        """
        if not change_type:
            change_type = self.get_change_type()
        change_types = {'DoesNotExist': 'NEW', 'Exists': 'KEYED', 'I': 'KEYED', 'U': 'KEYED', 'D': 'NEW'}
        if change_type not in change_types:
            raise ValueError('Change type must be any of {0}. Got {1}'.format(change_types.keys(), change_type))
        return change_types.get(change_type)

    def create_meta_data(self, instance=None, visit_instance=None):
        if instance and not visit_instance:
            visit_instance = self.get_visit_instance(instance)
        raise self.get_meta_data_model().DoesNotExist('Matching meta data instance does not exist. You need to refresh meta data for {0}'.format(visit_instance.appointment))

    def update_meta_data(self, instance, change_type, using=None):
        raise ImproperlyConfigured('Unable to update meta data.')


class EntryMetaDataManager(BaseMetaDataManager):

    meta_data_model = ScheduledEntryMetaData

    def create_meta_data(self, instance=None, visit_instance=None):
        """Creates a meta_data instance for the model at the time point (appointment) for the given registered_subject.

        May NOT be created based on visit reason."""
        if instance and not visit_instance:
            visit_instance = self.get_visit_instance(instance)
        if visit_instance.reason not in self.skip_create_visit_reasons:
            entry = Entry.objects.get(
                app_label=self.model._meta.app_label,
                model_name=self.model._meta.object_name.lower(),
                visit_definition=visit_instance.appointment.visit_definition
                )
            return self.get_meta_data_model().objects.create(
                appointment=visit_instance.appointment,
                registered_subject=visit_instance.appointment.registered_subject,
                due_datetime=entry.visit_definition.get_upper_window_datetime(visit_instance.report_datetime),
                entry=entry,
                entry_status=self.get_status()
                )
        return None

    def update_meta_data(self, instance, change_type, using=None):
        """Updates the meta_data instance.

        Called by the signal on post_save and pre_delete"""
        self.set_meta_data_instance(instance)
        if self.get_meta_data_instance():
            if change_type == 'D':
                self.get_meta_data_instance().report_datetime = None
            else:
                self.get_meta_data_instance().report_datetime = instance.report_datetime
            self.get_meta_data_instance().entry_status = self.get_status(change_type)
            self.get_meta_data_instance().save()
        self.run_rule_groups(self.get_visit_instance(instance))

    def run_rule_groups(self, visit_instance):
        """Runs rule groups for this visit instance."""
        site_rule_groups.update_for_visit_definition(visit_instance)

    def delete_meta_data(self, instance, using=None):
        """Deletes the meta data instance for this instance.

        Is this ever used?"""
        self.set_meta_data_instance(instance)
        self.get_meta_data_instance().delete()


class ReqisitionMetaDataStatusManager(BaseMetaDataManager):

    meta_data_model = ScheduledLabEntryBucket
