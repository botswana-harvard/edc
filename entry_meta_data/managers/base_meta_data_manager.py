from django.core.exceptions import ImproperlyConfigured
from django.db import models

from edc.constants import REQUIRED, NOT_REQUIRED, KEYED
from edc.core.bhp_common.utils import convert_from_camel
from edc.subject.appointment.models import Appointment


class BaseMetaDataManager(models.Manager):

    """Creates, updates or deletes meta data that tracks the entry status of models for a given visit."""
    meta_data_model = None
    skip_create_visit_reasons = ['missed', 'death', 'lost']  # list of visit reasons where meta data should not be created
    may_delete_entry_status = [REQUIRED, NOT_REQUIRED]

    def __init__(self, visit_model, visit_attr_name=None):
        self.name = None
        self._instance = None
        self._status = None
        self._meta_data_instance = None
        self._appointment_zero = None
        self._visit_instance = None
        self.visit_model = visit_model
        self.visit_attr_name = visit_attr_name or convert_from_camel(self.visit_model._meta.object_name)
        super(BaseMetaDataManager, self).__init__()

    def __repr__(self):
        return 'BaseMetaDataManager({0.instance!r})'.format(self)

    def __str__(self):
        return '({0.instance!r})'.format(self)

    @property
    def instance(self):
        return self._instance

    @instance.setter
    def instance(self, instance):
        self._instance = instance
#         self.status = None  # this is weird

    @property
    def query_options(self):
        return {self.visit_attr_name: self.visit_instance}

    @property
    def visit_instance(self):
        return self._visit_instance

    @visit_instance.setter
    def visit_instance(self, visit_instance):
        self._visit_instance = visit_instance
        self.appointment_zero = visit_instance.appointment
        self._meta_data_instance = None

    @property
    def appointment_zero(self):
        return self._appointment_zero

    @appointment_zero.setter
    def appointment_zero(self, appointment):
        if appointment.visit_instance == '0':
            self._appointment_zero = appointment
        else:
            self._appointment_zero = Appointment.objects.get(
                registered_subject=appointment.registered_subject,
                visit_definition=appointment.visit_definition,
                visit_instance='0')

    @property
    def meta_data_instance(self):
        """Returns the meta data instance using the meta data's "model" instance.

        Will be created if DoesNotExist."""
        if not self._meta_data_instance:
            try:
                self._meta_data_instance = self.meta_data_model.objects.get(**self.meta_data_query_options)
            except self.meta_data_model.DoesNotExist:
                self._meta_data_instance = self.create_meta_data()
            except ValueError as e:  # Cannot use None as a query value
                pass
            except AttributeError as e:
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
        """Figures out the the current status of the user model instance, KEYED or NEW/REQUIRED (not keyed).

        * Insert, Update and Delete (I, U, D) come from the signal.
        """
        change_types = {'DoesNotExist': REQUIRED,  # TODO: if REQUIRED is the default??
                        'Exists': KEYED,
                        'I': KEYED,
                        'U': KEYED,
                        'D': REQUIRED,  # TODO: if REQUIRED is the default??
                        REQUIRED: REQUIRED,
                        KEYED: KEYED,
                        NOT_REQUIRED: NOT_REQUIRED}
        if not change_type:
            change_type = 'Exists'  # KEYED
            if not self.instance:
                change_type = 'DoesNotExist'
        elif change_type in [REQUIRED, NOT_REQUIRED] and self.instance:
            change_type = KEYED
        if change_type not in change_types:
            raise ValueError('Change type must be any of {0}. Got {1}'.format(change_types.keys(), change_type))
        self._status = change_types.get(change_type)

    def create_meta_data(self):
        raise ImproperlyConfigured('Method must be defined in the child class')

    def update_meta_data(self, change_type=None):
        """Updates the meta_data's instance.

        Called by the signal on post_save and pre_delete"""
        if self.meta_data_instance:
            if change_type == 'D' or not self.instance:
                self.meta_data_instance.report_datetime = None
            else:
                self.meta_data_instance.report_datetime = self.instance.report_datetime
            self.status = change_type
            if not self.meta_data_instance.entry_status == self.status:
                self.meta_data_instance.entry_status = self.status
                self.meta_data_instance.save()

    def update_meta_data_from_rule(self, change_type):
        change_types = [REQUIRED, NOT_REQUIRED]
        if change_type not in change_types:
            raise ValueError('Change type must be any of {0}. Got {1}'.format(change_types, change_type))
        self.update_meta_data(change_type)

    def run_rule_groups(self):
        """Runs rule groups that use the data in this instance; that is, the model is a rule source model."""
        from edc.subject.rule_groups.classes import site_rule_groups
        return site_rule_groups.update_rules_for_source_model(self.model, self.visit_instance)
