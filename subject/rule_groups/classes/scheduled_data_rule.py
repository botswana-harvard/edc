import logging
from edc.entry_meta_data.classes import ScheduledEntryMetaDataHelper
from edc.entry_meta_data.models import ScheduledEntryMetaData
from .base_rule import BaseRule

logger = logging.getLogger(__name__)


class NullHandler(logging.Handler):
    def emit(self, record):
        pass
nullhandler = logger.addHandler(NullHandler())


class ScheduledDataRule(BaseRule):

    def __init__(self, *args, **kwargs):
        self.entry_class = ScheduledEntryMetaDataHelper
        self.meta_data_model = ScheduledEntryMetaData
        super(ScheduledDataRule, self).__init__(*args, **kwargs)

    def evaluate(self):
        """ Evaluate predicate and returns an action.

        Note that if the source model instance does not exist (has not been keyed yet) the predicate will be None
        and the rule will not be evaluated."""
        logger.debug('Evaluating rule {0} targeted for {1}.'.format(self, self.target_model._meta.object_name))
        action = None
        if self.predicate:
            if eval(self.predicate):
                action = self.consequent_action
            else:
                action = self.alternative_action
            action = self.is_valid_action(action)
        if action:
            action = action.upper()
        return action
