from django.core.exceptions import FieldError
from .base_entry import BaseEntry


class BaseScheduledEntry(BaseEntry):

    def set_target_model_base_cls(self):
        from edc.subject.visit_tracking.models import BaseVisitTracking
        self._target_model_base_cls = BaseVisitTracking

    def set_target_instance(self, target_instance=None):
        """ Sets the instance of the target model class if it can using the visit_model_instance."""
        self._target_instance = None
        if target_instance:
            self._target_instance = target_instance
            self.set_target_model(self._target_instance.__class__)
        elif self.get_visit_model_fieldname() and self.get_visit_model_instance():
            try:
                if self.get_target_model().objects.filter(**{self.get_visit_model_fieldname(): self.get_visit_model_instance()}).exists():
                    self._target_instance = self.get_target_model().objects.get(**{self.get_visit_model_fieldname(): self.get_visit_model_instance()})
            except FieldError as e:
                raise FieldError('Field {0} does not exist in model class {1}. Got {2}'.format(self.get_visit_model_fieldname(), self.get_target_model(), e))
            except:
                raise
        else:
            pass
