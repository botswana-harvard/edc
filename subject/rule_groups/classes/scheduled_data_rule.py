import logging
from edc.subject.entry.classes import ScheduledEntry
from edc.subject.entry.models import ScheduledEntryMetaData, Entry
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_tracking.models import BaseVisitTracking
from .base_rule import BaseRule

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class ScheduledDataRule(BaseRule):

    def set_entry_class(self):
        self._entry_class = ScheduledEntry

    def set_meta_data_model(self):
        self._meta_data_model = ScheduledEntryMetaData

    def get_action_list(self):
        return ['new', 'not_required']

    def set_meta_data_instance(self):
        """Sets the meta_data_instance for the target model knowing that the filter
        instance is either an instance of BaseVisitTracking or RegisteredSubject.

        Users should check if the set value is None which will be the case if the current visit
        does not contain the target model."""
        self._meta_data_instance = None
        app_label = self.get_target_model()._meta.app_label
        model_name = self.get_target_model()._meta.object_name.lower()
        if isinstance(self.get_filter_instance(), BaseVisitTracking):
            # filter on the visit model
            if self.get_meta_data_model().objects.filter(
                    entry__app_label=app_label,
                    entry__model_name=model_name,
                    registered_subject=self.get_filter_instance().appointment.registered_subject,
                    appointment=self.get_visit_model_instance().appointment).exists():
                self._meta_data_instance = self.get_meta_data_model().objects.get(
                    entry__app_label=app_label,
                    entry__model_name=model_name,
                    registered_subject=self.get_filter_instance().appointment.registered_subject,
                    appointment=self.get_visit_model_instance().appointment)
        elif isinstance(self.get_filter_instance(), RegisteredSubject):
            # filter on registered_subject
            if self.get_meta_data_model().objects.filter(
                    entry__app_label=app_label,
                    entry__model_name=model_name,
                    registered_subject=self.get_filter_instance(),
                    appointment=self.get_visit_model_instance().appointment).exists():
                self._meta_data_instance = self.get_meta_data_model().objects.get(
                    entry__app_label=app_label,
                    entry__model_name=model_name,
                    registered_subject=self.get_filter_instance(),
                    appointment=self.get_visit_model_instance().appointment)
        else:
            # filter instance is not None and is not an instance of anything we expect
            raise AttributeError('Attribute _meta_data_instance cannot be None. Given an instance that is neither an instance '
                                 'of BaseVisitTracking nor RegisteredSubject.')
        if not self._meta_data_instance:
            if self.get_target_model():
                logger.info('Target model {0} not found but referred to in rule {1}. Is this model name correct?'.format(self.get_target_model()._meta.object_name, self))
            else:
                if not Entry.objects.filter(app_label=app_label, model_name=model_name).exists():
                    logger.info('Warning: {0} referred to as a target model in rule {1} but is not scheduled in any visit definition.'.format(self.get_target_model()._meta.object_name, self))

    def evaluate(self):
        """ Evaluate predicate and calls ScheduleEntry class to updates bucket instance status.

        Note that if the source model instance does not exist (has not been keyed yet) the predicate will be None
        and the rule will not be evaluated."""
        logger.debug('Evaluating rule {0} targeted for {1}.'.format(self, self.get_target_model()._meta.object_name))
        predicate = self.get_predicate()
        if predicate:
            if eval(predicate):
                action = self.get_consequent_action()
            else:
                action = self.get_alternative_action()
            if self.is_valid_action(action):
                if self.get_meta_data_instance():  # make sure this visit has this target model
                    entry = self.get_entry_class()()
                    entry.update_status_from_rule(
                        action,
                        self.get_target_model(),
                        self.get_meta_data_instance(),
                        self.get_visit_model_instance(),
                        self.get_filter_instance(),  # visit_model_instance or registered subject instance
                        self.get_filter_fieldname(),
                        self.get_comment())  # visit_model fieldname or 'registered subject'
