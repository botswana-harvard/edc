from edc.core.bhp_common.utils import convert_from_camel

from edc.subject.visit_tracking.models import BaseVisitTracking

from ..models import BaseEntryMetaData


class BaseEntry(object):
    """ Base class for all classes that manage the entry state of additional, scheduled and unscheduled data."""
    def __init__(self, appointment, visit_model_or_instance, visit_model_attrname=None):
        self.appointment = appointment
        self.visit_model = visit_model_or_instance
        self.visit_model_attrname = visit_model_attrname
        self.visit_instance = visit_model_or_instance
        self.registered_subject = appointment.registered_subject

    @property
    def appointment_zero(self):
        if not self.appointment.visit_instance == 0:
            Appointment = self.appointment.__class__
            self._appointment_zero = Appointment.objects.get(
                registered_subject=self.appointment.registered_subject,
                visit_definition=self.appointment.visit_definition,
                visit_instance=0)
        else:
            self._appointment_zero = self.appointment
        return self._appointment_zero

    @property
    def visit_model(self):
        return self._visit_model

    @visit_model.setter
    def visit_model(self, model_or_instance):
        try:
            if issubclass(model_or_instance, BaseVisitTracking):
                self._visit_model = model_or_instance
        except TypeError:
            self._visit_model = model_or_instance.__class__

    @property
    def visit_model_attrname(self):
        return self._visit_model_attrname

    @visit_model_attrname.setter
    def visit_model_attrname(self, attrname):
        self._visit_model_attrname = attrname or convert_from_camel(self.visit_model._meta.object_name)

    @property
    def visit_instance(self):
        return self._visit_instance

    @visit_instance.setter
    def visit_instance(self, model_or_instance):
        if isinstance(model_or_instance, BaseVisitTracking):
            self._visit_instance = model_or_instance
        else:
            self._visit_instance = self.visit_model.objects.get(appointment=self.appointment)
        self.check_visit_model_reason_field(self._visit_instance)

    def check_visit_model_reason_field(self, visit_instance):
        """Confirms visit model has a reason attribute and the choices tuple uses required values correctly."""
        pass

    @property
    def filter_model_instance(self):
        return self._filter_model_instance

    @filter_model_instance.setter
    def filter_model_instance(self, filter_model_instance):
        """Sets the filter model instance to be the users visit model instance."""
        if filter_model_instance:
            if not isinstance(filter_model_instance, self.target_model_base_cls):
                AttributeError('Attribute _filter_model_instance must be an instance of {0}.'.format(self.target_model_base_cls))
        self._filter_model_instance = filter_model_instance

    def set_target_model_using_entry(self, entry_instance):
        self.target_model = entry_instance.get_model()

    @property
    def target_model(self):
        return self._target_model

    @target_model.setter
    def target_model(self, model):
        """Sets the model class that the entry model refers to."""
        if not issubclass(model, self.target_model_base_cls):
            AttributeError('Attribute model_cls must be an instance of {0}.'.format(self.target_model_base_cls))
        self._target_model = model
#         # if the class must match the instance, if not null the instance
#         if self._target_instance:
#             if not isinstance(self._target_instance, self._target_model):
#                 self._target_instance = None

    @property
    def meta_data_instance(self):
        return self._meta_data_instance

    @meta_data_instance.setter
    def meta_data_instance(self, meta_data_instance):
        if meta_data_instance:
            if not isinstance(meta_data_instance, BaseEntryMetaData):
                raise AttributeError('Attribute _meta_data_instance must be an instance of BaseEntryMetaData. Got {0}'.format(meta_data_instance))
        self._meta_data_instance = meta_data_instance

    @property
    def meta_data_model(self):
        return self._meta_data_model

    @meta_data_model.setter
    def meta_data_model(self, meta_data_model):
        if not issubclass(meta_data_model, BaseEntryMetaData):
            raise AttributeError('Attribute _meta_data_instance must be an subclass of BaseEntryMetaData. Got {0}'.format(meta_data_model))
        self._meta_data_model = meta_data_model

    def is_keyed(self):
        """ Indicates that the model instance exists (and is therefore keyed).  """
        if self.target_instance:
            return True
        else:
            return False

    def get_status(self, action):
        """Figures out the the current status of the user model instance, KEYED or NEW (not keyed)."""
        action = action.upper()
        action_terms = ['NEW', 'KEYED', 'NOT_REQUIRED', 'DELETE']
        if action not in action_terms:
            raise ValueError('Action must be %s. Got %s' % (action_terms, action))
        if self.is_keyed():
            retval = 'KEYED'
        else:
            retval = action
        if action == 'DELETE':
            retval = 'NEW'
        return retval

    def update_meta_data(self, action, report_datetime=None, comment=None):
        if not self.meta_data_instance:
            raise TypeError('Attribute for meta_data model instance cannot be None.')
        if not report_datetime:
            self.filter_model_instance.report_datetime
        self.meta_data_instance.report_datetime = report_datetime
        if comment:
            self.meta_data_instance.entry_comment = comment
        else:
            self.meta_data_instance.entry_comment = ''
        entry_status = self.get_status(action)
        self.meta_data_instance.entry_status = entry_status
        self.meta_data_instance.save()
