from django.core.exceptions import ImproperlyConfigured

from edc.subject.entry.models import LabEntry

from ..models import RequisitionMetaData

from .base_meta_data_manager import BaseMetaDataManager


class RequisitionMetaDataManager(BaseMetaDataManager):

    meta_data_model = RequisitionMetaData
    entry_model = LabEntry
    entry_attr = 'lab_entry'

    def __init__(self, visit_model, visit_attr_name=None):
        self._target_requisition_panel = None
        super(RequisitionMetaDataManager, self).__init__(visit_model, visit_attr_name)

    def __repr__(self):
        return 'RequisitionMetaDataManager({0.instance!r})'.format(self)

    def __str__(self):
        return '({0.instance!s})'.format(self)

    @property
    def target_requisition_panel(self):
        return self._target_requisition_panel

    @target_requisition_panel.setter
    def target_requisition_panel(self, target_requisition_panel):
        self._target_requisition_panel = target_requisition_panel
        self._meta_data_instance = None

    @property
    def query_options(self):
        return {self.visit_attr_name: self.visit_instance, 'panel__name': self.target_requisition_panel}

    @property
    def meta_data_query_options(self):
        """Returns the options used to query the meta data model for the meta_data_instance."""
        return {'appointment': self.appointment_zero,
                '{0}__app_label'.format(self.entry_attr): self.model._meta.app_label,
                '{0}__model_name'.format(self.entry_attr): self.model._meta.object_name.lower(),
                '{0}__requisition_panel__name__iexact'.format(self.entry_attr): self.target_requisition_panel}

    def create_meta_data(self):
        """Creates a meta_data instance for the model at the time point (appointment) for the given registered_subject.

        might return None and meta data not created based on visit reason (e.g. missed)."""
        if self.visit_instance.reason not in self.skip_create_visit_reasons:
            try:
                lab_entry = self.entry_model.objects.get(
                    app_label=self.model._meta.app_label.lower(),
                    model_name=self.model._meta.object_name.lower(),
                    visit_definition=self.appointment_zero.visit_definition,
                    requisition_panel=self.target_requisition_panel,
                    )
            except self.entry_model.DoesNotExist:
                raise ImproperlyConfigured('LabEntry matching query does not exist. Model {0}.Check your'
                                           ' visit schedule configuration or rule groups.'.format(self.model))
            return self.meta_data_model.objects.create(
                appointment=self.appointment_zero,
                registered_subject=self.appointment_zero.registered_subject,
                due_datetime=lab_entry.visit_definition.get_upper_window_datetime(self.visit_instance.report_datetime),
                lab_entry=lab_entry,
                entry_status=lab_entry.default_entry_status,
                )
        return None

    @property
    def default_entry_status(self):
        return self.meta_data_instance.lab_entry.default_entry_status
