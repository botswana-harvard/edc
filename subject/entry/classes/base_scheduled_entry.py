from django.core.exceptions import FieldError

from edc.subject.visit_tracking.models import BaseVisitTracking

from .base_entry import BaseEntry


class BaseScheduledEntry(BaseEntry):

    def __init__(self, *args, **kwargs):
        self.target_model_base_cls = BaseVisitTracking
        super(BaseScheduledEntry, self).__init__(*args, **kwargs)

    @property
    def target_instance(self):
        return self._target_instance

    @target_instance.setter
    def target_instance(self, target_instance):
        """ Sets the instance of the target model class if it can using the visit_model_instance."""
        self._target_instance = target_instance
        if self._target_instance:
            self.target_model = self._target_instance.__class__
        elif self.visit_model_fieldname and self.visit_model_instance:
            try:
                if self.target_model.objects.filter(**{self.visit_model_fieldname: self.visit_model_instance}).exists():
                    self._target_instance = self.target_model.objects.get(**{self.visit_model_fieldname: self.visit_model_instance})
                    self.target_model = self._target_instance.__class__
            except FieldError as e:
                raise FieldError('Field {0} does not exist in model class {1}. Got {2}'.format(self.visit_model_fieldname, self.target_model, e))
            except:
                raise
        else:
            pass
