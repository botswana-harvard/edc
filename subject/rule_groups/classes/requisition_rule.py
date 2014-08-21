from edc.core.bhp_common.utils import convert_from_camel

from .base_rule import BaseRule


class RequisitionRule(BaseRule):
    """A RequisitionRule is instantiated as a class attribute of a rule group."""

    def __init__(self, *args, **kwargs):
        super(RequisitionRule, self).__init__(*args, **kwargs)
        if 'target_requisition_panels' not in kwargs:
            raise KeyError('{0} is missing required attribute \'target_requisition_panels\''.format(self.__class__.__name__))
        from edc.entry_meta_data.helpers import RequisitionMetaDataHelper
        from edc.entry_meta_data.models import RequisitionMetaData
        self.entry_class = RequisitionMetaDataHelper
        self.meta_data_model = RequisitionMetaData
        self.target_requisition_panels = kwargs.get('target_requisition_panels')

    def run(self, visit_instance):
        """ Evaluate the rule for the requisition model for each requisition panel."""
        for target_model in self.target_model_list:  # is a requisition model(s)
            for target_requisition_panel in self.target_requisition_panels:
                self.target_model = target_model
                self.visit_instance = visit_instance
                self.registered_subject = self.visit_instance.appointment.registered_subject
                self.visit_attr_name = convert_from_camel(self.visit_instance._meta.object_name)
                self._source_instance = None
                self._target_instance = None
                change_type = self.evaluate()
                if change_type:
                    self.target_model.entry_meta_data_manager.visit_instance = self.visit_instance
                    self.target_model.entry_meta_data_manager.target_requisition_panel = target_requisition_panel
                    try:
                        self.target_model.entry_meta_data_manager.instance = self.target_model.objects.get(**self.target_model.entry_meta_data_manager.query_options)
                    except self.target_model.DoesNotExist:
                        self.target_model.entry_meta_data_manager.instance = None
                    self.target_model.entry_meta_data_manager.update_meta_data_from_rule(change_type)
