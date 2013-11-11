from edc.core.bhp_common.utils import convert_from_camel
# from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.subject.visit_tracking.models import BaseVisitTracking

from ..models import BaseEntryMetaData


class BaseEntry(object):
    """ Base class for all classes that manage the entry state of additional, scheduled and unscheduled data."""
    def __init__(self, appointment, visit_model_or_instance, visit_model_attrname=None):
        self._filter_fieldname = None  # field to filter the target_model
        self._filter_model_instance = None  # instance of field to filter the user model
        self._target_model = None
        self._meta_data_model = None  # for example, ScheduledEntryMetaData, AdditionalEnrtyBucket
        self._meta_data_instance = None
        self._target_model_base_cls = None  # for error reporting
#         self._content_type_map = None  # to help get the correct instance from the model 'Entry'
        self._target_instance = None
        self._visit_model_fieldname = None
        self._visit_model_base_cls = None

        self._appointment = None
        self._appointment_zero = None
        self._registered_subject = None
        self._visit_model = None
        self._visit_model_attrname = None
        self._visit_instance = None
        self.set_appointment(appointment)
        self.set_appointment_zero()
        self.set_visit_model(visit_model_or_instance)
        self.set_visit_model_attrname(visit_model_attrname)
        self.set_visit_instance(visit_model_or_instance)
        self.set_registered_subject()
        self.set_meta_data_model()

    def set_appointment(self, appointment):
        if appointment:
            self._appointment = appointment
        else:
            raise AttributeError('Attribute appointment may not be None.')

    def get_appointment(self):
        return self._appointment

    def set_appointment_zero(self):
        if not self.get_appointment().visit_instance == 0:
            Appointment = self.get_appointment().__class__
            self._appointment_zero = Appointment.objects.get(
                registered_subject=self.get_appointment().registered_subject,
                visit_definition=self.get_appointment().visit_definition,
                visit_instance=0)
        else:
            self._appointment_zero = self.get_appointment()

    def get_appointment_zero(self):
        return self._appointment_zero

    def set_visit_model(self, model_or_instance):
        try:
            if issubclass(model_or_instance, BaseVisitTracking):
                self._visit_model = model_or_instance

        except TypeError:
            self._visit_model = model_or_instance.__class__
        if not self._visit_model:
            raise AttributeError('Attribute visit_model may not be None.')

    def get_visit_model(self):
        return self._visit_model

    def set_visit_model_attrname(self, attrname):
        self._visit_model_attrname = attrname or convert_from_camel(self.get_visit_model()._meta.object_name)

    def get_visit_model_attrname(self):
        return self._visit_model_attrname

    def set_visit_instance(self, model_or_instance):
        if isinstance(model_or_instance, BaseVisitTracking):
            self._visit_instance = model_or_instance
        else:
            self._visit_instance = self.get_visit_model().objects.get(appointment=self.get_appointment())
        self.check_visit_model_reason_field(self._visit_instance)

    def get_visit_instance(self):
        return self._visit_instance

    def set_registered_subject(self):
        self._registered_subject = self.get_appointment().registered_subject

    def get_registered_subject(self):
        return self._registered_subject

#     def reset(self):
#         self._meta_data_instance = None
#         self._target_instance = None
#         self._filter_model_instance = None
#         self._visit_instance = None
#         self.set_visit_instance(visit_instance)

#     def set_visit_model_base_cls(self):
#         self._visit_model_base_cls = BaseVisitTracking

#     def get_visit_model_base_cls(self):
#         return self._visit_model_base_cls

#     def set_visit_instance(self, visit_instance=None):
#         if not isinstance(visit_instance, self.get_visit_model_base_cls()):
#             raise TypeError('Parameter \'visit_instance\' must be an instance of BaseVisitTracking. Got {0}'.format(visit_instance))
#         self.check_visit_model_reason_field(visit_instance)
#         self._visit_instance = visit_instance
#         if not self._visit_instance:
#             raise AttributeError('Attribute _visit_instance cannot be None')

    def check_visit_model_reason_field(self, visit_instance):
        """Confirms visit model has a reason attribute and the choices tuple uses required values correctly."""
        pass

    def set_filter_fieldname(self, filter_field_name=None):
        """ Returns the field name to be used to \'get\'  the target_instance or filter the user model class.

        Users need to override this

        For example may return \'registered_subject\' for meta_data model classes that do
        not have a visit model foreign key.
        """
        if self._filter_fieldname is None:
            raise TypeError('Attribute filter_fieldname cannot be None. Override this method in the subclass.')

#     def set_visit_model_fieldname(self, visit_model_fieldname=None):
#         """Returns the field name for the foreignkey that points to the visit model."""
#         self._visit_model_fieldname = None
#         if visit_model_fieldname:
#             self._visit_model_fieldname = visit_model_fieldname
#         else:
#             if self.get_target_model():
#                 # look for a field value that is a base of
#                 for field in self.get_target_model()._meta.fields:
#                     if field.rel:
#                         if issubclass(field.rel.to, self.get_visit_model_base_cls()):
#                             self._visit_model_fieldname = field.name
#                             break
#             else:
#                 pass
#         if not self._visit_model_fieldname:
#             raise AttributeError('Attribute _visit_model_fieldname cannot be None. Check the models listed in your visit definition.')
#
#     def get_visit_model_fieldname(self):
# #         if not self._visit_model_fieldname:
# #             self.set_visit_model_fieldname()
#         return self._visit_model_fieldname

    def set_target_model_base_cls(self):
        """Users need to override this to set to something like BaseVisitTracking."""
        if self._target_model_base_cls is None:
            raise AttributeError('Attribute _target_model_base_cls cannot be None.')

    def get_target_model_base_cls(self):
#         if not self._target_model_base_cls:
#             self.set_target_model_base_cls()
        return self._target_model_base_cls

    def set_filter_model_instance(self, filter_model_instance=None):
        """Sets the filter model instance to be the users visit model instance."""
        if filter_model_instance:
            if not isinstance(filter_model_instance, self.get_target_model_base_cls()):
                AttributeError('Attribute _filter_model_instance must be an instance of {0}.'.format(self.get_target_model_base_cls()))
            self._filter_model_instance = filter_model_instance

    def get_filter_fieldname(self):
#         if not self._filter_fieldname:
#             self.set_filter_fieldname()
        return self._filter_fieldname

    def get_filter_model_instance(self):
#         if not self._filter_model_instance:
#             self.set_filter_model_instance()
        return self._filter_model_instance

    def set_target_model_using_entry(self, entry_instance):
        self.set_target_model(entry_instance.get_model())

    def set_target_model(self, model_cls=None):
        """Sets the model class that the entry model refers to."""
        if model_cls is None:
            raise AttributeError('Attribute model_cls cannot be None.')
        if not issubclass(model_cls, self.get_target_model_base_cls()):
            AttributeError('Attribute model_cls must be an instance of {0}.'.format(self.get_target_model_base_cls()))
        self._target_model = model_cls
        # if the class must match the instance, if not null the instance
        if self._target_instance:
            if not isinstance(self._target_instance, self._target_model):
                self._target_instance = None

    def get_target_model(self):
#         if not self._target_model:
#             self.set_target_model()
        return self._target_model

    def set_target_instance(self, target_instance=None):
        raise TypeError("Method must be overridden")

    def get_target_instance(self):
        return self._target_instance

    def set_meta_data_instance(self, meta_data_instance=None):
        if meta_data_instance:
            if not isinstance(meta_data_instance, BaseEntryMetaData):
                raise AttributeError('Attribute _meta_data_instance must be an instance of BaseEntryMetaData. Got {0}'.format(meta_data_instance))
        self._meta_data_instance = meta_data_instance

#     def set_meta_data_instance_with_id(self, meta_data_instance_id):
#         self.set_meta_data_instance(self.get_meta_data_model().objects.get(pk=meta_data_instance_id))

    def get_meta_data_instance(self):
#         if not self._meta_data_instance:
#             self.set_meta_data_instance()
        return self._meta_data_instance

    def set_meta_data_model(self):
        """Users need to override this to set with something like ScheduledEnrtyBucket."""
        if self._meta_data_model is None:
            raise AttributeError('Attribute _meta_data_model cannot be None.')

    def get_meta_data_model(self):
        return self._meta_data_model

#     def set_content_type_map(self, content_type_map=None):
#         if content_type_map:
#             self._content_type_map = content_type_map
#         else:
#             model = self.get_target_model() or self.get_target_instance()
#             if model:
#                 self._content_type_map = ContentTypeMap.objects.get(
#                     app_label=self.model._meta.app_label,
#                     name=self.model._meta.verbose_name)
#             else:
#                 self._content_type_map = None
# 
#     def get_content_type_map(self):
#         return self._content_type_map

    def is_keyed(self):
        """ Indicates that the model instance exists (and is therefore keyed).  """
        if self.get_target_instance():
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
        meta_data_instance = self.get_meta_data_instance()
        if not meta_data_instance:
            raise TypeError('Attribute for meta_data model instance cannot be None.')
        if not report_datetime:
            self.get_filter_model_instance().report_datetime
        meta_data_instance.report_datetime = report_datetime
        if comment:
            meta_data_instance.entry_comment = comment
        else:
            meta_data_instance.entry_comment = ''
        entry_status = self.get_status(action)
        meta_data_instance.entry_status = entry_status
        meta_data_instance.save()
