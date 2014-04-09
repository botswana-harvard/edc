from edc.subject.entry.models import LabEntry

from ..models import RequisitionMetaData

from .base_meta_data_helper import BaseMetaDataHelper


class RequisitionMetaDataHelper(BaseMetaDataHelper):

    meta_data_model = RequisitionMetaData
    entry_model = LabEntry
    entry_attr = 'lab_entry'

    def __repr__(self):
        return 'RequisitionMetaDataHelper({0.instance!r})'.format(self)

    def __str__(self):
        return '({0.instance!r})'.format(self)

    def add_or_update_for_visit(self):
        """ Loops thru the list of entries configured for the visit_definition and calls the entry_meta_data_manager for each model.

        The visit definition comes instance."""
        for lab_entry in self.entry_model.objects.filter(visit_definition=self.visit_instance.appointment.visit_definition):
            model = lab_entry.get_model()
            model.entry_meta_data_manager.visit_instance = self.visit_instance
            model.entry_meta_data_manager.target_requisition_panel = lab_entry.requisition_panel
            try:
                model.entry_meta_data_manager.instance = model.objects.get(**model.entry_meta_data_manager.query_options)
            except model.DoesNotExist:
                pass
            model.entry_meta_data_manager.update_meta_data()
            if model.entry_meta_data_manager.instance:
                model.entry_meta_data_manager.run_rule_groups()
