from edc.core.bhp_common.utils import convert_from_camel
from edc.entry_meta_data.models import RequisitionMetaData

from .base_scheduled_entry_context import BaseScheduledEntryContext


class RequisitionContext(BaseScheduledEntryContext):

    """A Class used by the dashboard when rendering the list of scheduled entries to display under "Scheduled Forms"."""

    meta_data_model = RequisitionMetaData

    def __init__(self, meta_data_instance, appointment, visit_model, requisition_model):
        self.requisition_model = requisition_model
        super(RequisitionContext, self).__init__(meta_data_instance, appointment, visit_model)

    def contribute_to_context(self, context):
        context.update({'label': self.meta_data_instance.lab_entry.panel.edc_name})
        if self.instance:
            context.update({'requisition_identifier': self.instance.requisition_identifier})
            context.update({'panel': self.instance.panel.pk})
        return context

    @property
    def model(self):
        return self.requisition_model

    @property
    def instance(self):
        """Sets to the model instance referred to by the scheduled lab entry."""
        if not self._instance:
            options = {convert_from_camel(self.visit_instance._meta.object_name): self.visit_instance, 'panel': self.meta_data_instance.lab_entry.panel.pk}
            if self.model.objects.filter(**options):
                self._instance = self.model.objects.get(**options)
        return self._instance
