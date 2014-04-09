# from edc.entry_meta_data.helpers import ScheduledEntryMetaDataHelper
# from edc.entry_meta_data.models import ScheduledEntryMetaData

from .base_rule import BaseRule


class ScheduledDataRule(BaseRule):
    """
    A ScheduledDataRule is instantiated as a class attribute of a rule group.

    * If not within a rule group, rules don't do anything...don't work;
    * The RuleGroup's Meta class determines the 'source' model and 'source_fk' model;
    * The field criteria specified in the logic refers to fields in the source model;
    * The source model has an FK attribute pointing to an instance of the source_fk model (with the exception of RegisteredSubject);
    * The rule specifies the target model(s) for whose meta data will be evaluated and possibly updated (e.g. set NEW to NOT REQUIRED);
    * Target models always have an attr pointing to an instance of the visit instance;
    * That is, Target models are scheduled models;
    * A rule changes a 'target' model's metadata entry status value.

    ..see_also:: For more about the meta data that rules operate on see module 'entry_meta_data'.

    ..see_also:: The tests also show most of the functionality of rules and rule groups.

    Usage::
        class ResourceUtilizationRuleGroup(RuleGroup):
            out_patient = ScheduledDataRule(
                logic=Logic(
                    predicate=(('out_patient', 'equals', 'no'), ('out_patient', 'equals', 'REF', 'or')),
                    consequence='not_required',
                    alternative='new'),
                target_model=['outpatientcare'])
        class Meta:
            app_label = 'bcpp_subject'
            source_fk = (SubjectVisit, 'subject_visit')
            source_model = ResourceUtilization
    """

    def __init__(self, *args, **kwargs):
        from edc.entry_meta_data.helpers import ScheduledEntryMetaDataHelper
        from edc.entry_meta_data.models import ScheduledEntryMetaData
        super(ScheduledDataRule, self).__init__(*args, **kwargs)
        self.entry_class = ScheduledEntryMetaDataHelper
        self.meta_data_model = ScheduledEntryMetaData
        self.helper_class_instance = kwargs.get('helper_class') if kwargs.get('helper_class', None) else None
        self.helper_class_attr = kwargs.get('helper_class_attr')

    def evaluate(self):
        """ Evaluates the predicate and returns an action.

        ..note:: if the source model instance does not exist (has not been keyed yet) the predicate will be None
        and the rule will not be evaluated."""
#         try:
#             #Try instantiate helper_class, if its already instantiated from other rules, then ou will  get a TypeError, Ignore it.
#             self.helper_class_instance = self.helper_class_instance(self.visit_instance) if self.helper_class_instance else None
#         except TypeError as e:
#             pass
        helper_class_instance = None
        helper_class_instance = self.helper_class_instance(self.visit_instance) if self.helper_class_instance else None
        action = None
        predicate = None
        method_result = None
        if helper_class_instance:
            method_result = str(getattr(helper_class_instance, self.helper_class_attr))
        else:
            predicate = self.predicate
        to_evaluate = predicate or method_result
        if to_evaluate:
            if eval(to_evaluate):
                action = self.consequent_action
            else:
                if self.alternative_action != 'none':
                    action = self.alternative_action
            action = self.is_valid_action(action)
        if action:
            action = action.upper()
        return action
