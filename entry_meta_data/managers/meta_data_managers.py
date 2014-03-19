from django.core.exceptions import ImproperlyConfigured
from django.db import models

from edc.core.bhp_common.utils import convert_from_camel
from edc.subject.appointment.models import Appointment
from edc.subject.entry.models import Entry
from edc.subject.entry.models import LabEntry
from edc.subject.rule_groups.classes import site_rule_groups
from edc.subject.visit_tracking.models import BaseVisitTracking

from ..models import RequisitionMetaData, ScheduledEntryMetaData


class BaseMetaDataManager(models.Manager):

    """Creates, updates or deletes meta data that tracks the entry status of models for a given visit."""
    meta_data_model = None
    skip_create_visit_reasons = ['missed', 'death', 'lost']  # list of visit reasons where meta data should not be created
    may_delete_entry_status = ['NEW', 'NOT_REQUIRED']

    def __init__(self, visit_model, visit_attr_name=None):
        self.visit_model = visit_model
        self.visit_attr_name = visit_attr_name or convert_from_camel(self.visit_model._meta.object_name)
        super(BaseMetaDataManager, self).__init__()

    def __repr__(self):
        if self._instance:
            name = self._instance
        else:
            name = 'model with {0}'.self._visit_instance
        return '{0}.{1}'.format(self.model._meta.object_name, name)

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, instance_or_visit_instance):
        """Sets the model instance referred to by the entry meta data directly or by doing a lookup with the visit instance.

        self.instance is an instance of self.model or None"""
        self._instance = None
        if isinstance(instance_or_visit_instance, self.model):
            self._instance = instance_or_visit_instance
            self.visit_instance = getattr(self.instance, self.visit_attr_name)
        elif isinstance(instance_or_visit_instance, BaseVisitTracking):
            if super(BaseMetaDataManager, self).filter(**{self.visit_attr_name: instance_or_visit_instance}):
                self._instance = super(BaseMetaDataManager, self).get(**{self.visit_attr_name: instance_or_visit_instance})
            self.visit_instance = instance_or_visit_instance
        self.appointment_zero = self.visit_instance.appointment
        # reset meta data instance
        self._meta_data_instance = None
        # reset status
        self.status = None

    @property
    def appointment_zero(self):
        return self._appointment_zero

    @appointment_zero.setter
    def appointment_zero(self, appointment):
        if appointment.visit_instance == '0':
            self._appointment_zero = appointment
        else:
            self._appointment = Appointment.objects.get(
                registered_subject=appointment.registered_subject,
                visit_definition=appointment.visit_definition,
                visit_instance=0)

    @property
    def meta_data_instance(self):
        """Returns the meta data instance using the meta data's "model" instance.

        Will be created if DoesNotExist."""
        if not self._meta_data_instance:
            try:
                self._meta_data_instance = self.meta_data_model.objects.get(**self.meta_data_query_options)
            except self.meta_data_model.DoesNotExist:
                self._meta_data_instance = self.create_meta_data()
            except AttributeError:
                # 'NoneType' object has no attribute 'panel'
                pass
        return self._meta_data_instance

    @property
    def meta_data_query_options(self):
        """Returns the options to query on the meta data model."""
        return {'appointment': self.appointment_zero,
                '{0}__app_label'.format(self.entry_attr): self.model._meta.app_label,
                '{0}__model_name'.format(self.entry_attr): self.model._meta.object_name.lower()}

    @property
    def status(self):
        return self._status

    @status.setter
    def status(self, change_type):
        """Figures out the the current status of the user model instance, KEYED or NEW (not keyed).

        * Insert, Update and Delete (I, U, D) come from the signal.
        """
        change_types = {'DoesNotExist': 'NEW', 'Exists': 'KEYED', 'I': 'KEYED', 'U': 'KEYED', 'D': 'NEW'}
        if not change_type:
            change_type = 'Exists'
            if not self.instance:
                change_type = 'DoesNotExist'
        if change_type not in change_types:
            raise ValueError('Change type must be any of {0}. Got {1}'.format(change_types.keys(), change_type))
        self._status = change_types.get(change_type)

    def create_meta_data(self):
        raise ImproperlyConfigured('Method must be defined in the child class')

    def update_meta_data(self, model_or_visit_instance, change_type=None, using=None):
        """Updates the meta_data's instance.

        Called by the signal on post_save and pre_delete"""
        self.instance = model_or_visit_instance
        if self.meta_data_instance:
            if self.meta_data_instance.entry_status != 'NOT_REQUIRED':
                if change_type == 'D' or not self.instance:
                    self.meta_data_instance.report_datetime = None
                else:
                    self.meta_data_instance.report_datetime = self.instance.report_datetime
                self.status = change_type
                self.meta_data_instance.entry_status = self.status
                self.meta_data_instance.save()

    def update_meta_data_from_rule(self, model_or_visit_instance, change_type, using=None):
        change_types = ['NEW', 'NOT_REQUIRED']
        if change_type not in change_types:
            raise ValueError('Change type must be any of {0}. Got {1}'.format(change_types, change_type))
        if self.meta_data_instance.entry_status != change_type:
            self.meta_data_instance.entry_status = change_type
            self.meta_data_instance.save()

    def delete_meta_data(self, model_or_visit_instance):
        self.instance = model_or_visit_instance
        if self.meta_data_instance and not self.instance and self.status in self.may_delete_entry_status:
            self.meta_data_instance.delete()

    def run_rule_groups(self):
        """Runs rule groups that use the data in this instance; that is, the model is a rule source model."""
        return site_rule_groups.update_rules_for_source_model(self.model, self.visit_instance)


class EntryMetaDataManager(BaseMetaDataManager):

    meta_data_model = ScheduledEntryMetaData
    entry_model = Entry
    entry_attr = 'entry'

    def create_meta_data(self):
        """Creates a meta_data instance for the model at the time point (appointment) for the given registered_subject.

        might NOT be created based on visit reason."""
        if self.visit_instance.reason not in self.skip_create_visit_reasons:
            try:
                entry = self.entry_model.objects.get(
                    app_label=self.model._meta.app_label.lower(),
                    model_name=self.model._meta.object_name.lower(),
                    visit_definition=self.appointment_zero.visit_definition
                    )
            except self.entry_model.DoesNotExist:
                raise ImproperlyConfigured('Entry matching query does not exist. Model {0}.Check your'
                                           ' visit schedule configuration or rule groups.'.format(self.model))
            return self.meta_data_model.objects.create(
                appointment=self.appointment_zero,
                registered_subject=self.appointment_zero.registered_subject,
                due_datetime=entry.visit_definition.get_upper_window_datetime(self.visit_instance.report_datetime),
                entry=entry,
                entry_status=self.status
                )
        return None


class RequisitionMetaDataManager(BaseMetaDataManager):

    meta_data_model = RequisitionMetaData
    entry_model = LabEntry
    entry_attr = 'lab_entry'

    def __init__(self, visit_model, visit_attr_name=None):
        self._target_requisition_panel = None
        super(RequisitionMetaDataManager, self).__init__(visit_model, visit_attr_name)

    @property
    def meta_data_query_options(self):
        """Returns the options used to query the meta data model for the meta_data_instance."""
        return {'appointment': self.appointment_zero,
                '{0}__app_label'.format(self.entry_attr): self.model._meta.app_label,
                '{0}__model_name'.format(self.entry_attr): self.model._meta.object_name.lower(),
                '{0}__requisition_panel__name__iexact'.format(self.entry_attr): self.target_requisition_panel}

    def create_meta_data(self):
        """Creates one meta_data instance for each requisition_panel for the requisition model at the time point (appointment) for the given registered_subject.

        might NOT be created based on visit reason."""
        meta_data_instances = []
        meta_data_instance = None

        if self.instance:
            self.target_requisition_panel = self.instance.panel

        if self.visit_instance.reason not in self.skip_create_visit_reasons:
            lab_entries = self.entry_model.objects.filter(
                app_label=self.model._meta.app_label.lower(),
                model_name=self.model._meta.object_name.lower(),
                visit_definition=self.appointment_zero.visit_definition,
                )
            if not lab_entries:
                raise ImproperlyConfigured('LabEntry matching queries do not exist. Model {0}.Check your'
                                           ' visit schedule configuration or rule groups.'.format(self.model))
            for lab_entry in lab_entries:
                options = dict(
                    appointment=self.appointment_zero,
                    registered_subject=self.appointment_zero.registered_subject,
                    due_datetime=lab_entry.visit_definition.get_upper_window_datetime(self.visit_instance.report_datetime),
                    lab_entry=lab_entry,
                    entry_status=self.status)
                try:
                    meta_data_instance = self.meta_data_model.objects.get(**options)
                except self.meta_data_model.DoesNotExist:
                    meta_data_instance = self.meta_data_model.objects.create(**options)
                meta_data_instances.append(meta_data_instance)
        if meta_data_instances:
            try:
                meta_data_instance = [item for item in meta_data_instances if item.lab_entry.requisition_panel == self.target_requisition_panel][0]
            except IndexError:
                pass
        return meta_data_instance

    def update_meta_data(self, model_or_visit_instance, change_type=None, using=None):
        """Updates the meta_data's instances by requisition_panel.

        Called by the signal on post_save and pre_delete"""
        self.instance = model_or_visit_instance
        if self.instance:
            super(RequisitionMetaDataManager, self).update_meta_data(model_or_visit_instance, change_type, using)
        else:
            self.create_meta_data()

    def update_meta_data_from_rule(self, model_or_visit_instance, change_type, target_requisition_panel, using=None):
        self.target_requisition_panel = target_requisition_panel
        super(RequisitionMetaDataManager, self).update_meta_data_from_rule(model_or_visit_instance, change_type, using)

    @property
    def target_requisition_panel(self):
        return self._target_requisition_panel

    @target_requisition_panel.setter
    def target_requisition_panel(self, target_requisition_panel):
        """Sets the target_requisition_panel to that of the instance otherwise the passed parameter"""
        try:
            self._target_requisition_panel = self.instance.panel
        except:
            self._target_requisition_panel = target_requisition_panel
