from edc.core.bhp_common.utils import convert_from_camel

from edc.lab.lab_requisition.models import BaseRequisition

from .base_scheduled_entry_context import BaseScheduledEntryContext


class ScheduledRequisitionContext(BaseScheduledEntryContext):

    """A Class used by the dashboard when rendering the list of scheduled entries to display under "Scheduled Forms"."""

    def __init__(self, scheduled_entry, appointment, visit_model, requisition_model):
        self._requisition_model = None
        self.set_requisition_model(requisition_model)
        super(ScheduledRequisitionContext, self).__init__(scheduled_entry, appointment, visit_model)

    def contribute_to_context(self, context):
        if self.get_model_inst():
            context.update({'requisition_identifier': self.get_model_inst().requisition_identifier})
            context.update({'panel': self.get_model_inst().panel.pk})
        return context

    def get_entry_label(self):
        return self.get_entry().panel.edc_name

    def set_requisition_model(self, value):
        self._requisition_model = value
        if not value:
            raise TypeError('Expected a subclass of BaseRequsition. Got {0}.'.format(value))
        if not issubclass(value, BaseRequisition):
            raise TypeError('Expected a subclass of BaseRequsition. Got {0}.'.format(value))

    def get_requisition_model(self):
        return self._requisition_model

    def get_app_label(self):
        return self.get_requisition_model()._meta.app_label

    def get_model_name(self):
        return self.get_requisition_model()._meta.object_name.lower()

    def set_entry(self):
        """Sets to the Entry instance related to the scheduled entry."""
        self._entry = self.get_scheduled_entry().lab_entry

    def get_panel(self):
        return self.get_entry().panel

    def set_model_inst(self):
        """Sets to the model instance refered to by the scheduled entry."""
        self._model_inst = None
        options = {convert_from_camel(self.get_visit_model_instance()._meta.object_name): self.get_visit_model_instance(), 'panel': self.get_panel()}
        if self.get_model_cls().objects.filter(**options):
            self._model_inst = self.get_model_cls().objects.get(**options)

    def get_group_title(self):
        return ''
