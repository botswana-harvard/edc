import re

from datetime import date, datetime

from django.db.models import get_model, IntegerField

from edc.core.bhp_common.utils import convert_from_camel
from edc.subject.consent.classes import ConsentHelper
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.visit_tracking.models import BaseVisitTracking

from .logic import Logic


class BaseRule(object):
    """Base class for all rules.

    Rules are class attributes of a rule group.

    ..see_also: comment on :module:`ScheduledDataRule`"""

    operators = ['equals', 'eq', 'gt', 'gte', 'lt', 'lte', 'ne', '!=', '==', 'in', 'not in']
    action_list = ['new', 'not_required', 'none']

    def __init__(self, **kwargs):

        self._source_instance = None
        self._predicate = None
        self._predicate_comparative_value = None
        self._predicate_field_value = None
        self._visit_instance = None
        self._target_model = None
        self._unresolved_predicate = None

        self.name = None
        self.source_model = None
        self.source_fk_model = None
        self.source_fk_attr = None
        self.target_model_list = []
        self.filter_model_attr = None
        self.filter_model_cls = None
        self.target_model_names = []

        if 'logic' in kwargs:
            self.logic = kwargs.get('logic')
        if 'target_model' in kwargs:
            self.target_model_list = kwargs.get('target_model')

    def __repr__(self):
        return self.name or self.source_model or self.__class__.__name__

    def run(self, visit_instance):
        """ Evaluate the rule for each model class in the target model list."""
        for target_model in self.target_model_list:
            self.target_model = target_model
            self.visit_instance = visit_instance
            self.registered_subject = self.visit_instance.appointment.registered_subject
            self.visit_attr_name = convert_from_camel(self.visit_instance._meta.object_name)

            self._source_instance = None
            self._target_instance = None

            change_type = self.evaluate()
            if change_type:
                # try to update target model's entry meta data, if it has not been keyed
                # If it exists, The target model instance will be set by querying the target model on the visit instance.
                # See instance property in entry_meta_data_manager
                self.target_model.entry_meta_data_manager.instance = self.visit_instance
                if not self.target_model.entry_meta_data_manager.instance:
                    self.target_model.entry_meta_data_manager.update_meta_data_from_rule(self.visit_instance, change_type)

    def evaluate(self):
        raise AttributeError('Evaluate should be overridden. Nothing to do.')

    @property
    def logic(self):
        return self._logic

    @logic.setter
    def logic(self, logic):
        if isinstance(logic, Logic):
            self._logic = logic
            if self._logic is None:
                raise AttributeError('Logic cannot be None.')
            if self.is_valid_action(logic.consequence):
                self.consequent_action = logic.consequence
            if self.is_valid_action(logic.alternative):
                self.alternative_action = logic.alternative
            if 'comment' in dir(logic):
                self.comment = logic.comment
        else:
            raise AttributeError('Attribute \'logic\' must be an instance of class Logic.')

    def is_valid_action(self, action):
        """Returns true if the action is in the list of valid actions or, if invalid action, raises an error."""
        if action:
            if action.lower() not in self.action_list:
                raise TypeError('Encountered an invalid action \'{0}\' when parsing additional rule. '
                                'Valid actions are \'{1}\'.'.format(action, ', '.join(self.action_list)))
        return action

    def get_operator_from_word(self, word, a, b):
        """Returns the operator from the 'word' used in the predicate, for example 'equals' returns '=='.

            Args:
                a = field_value
                b = comparative_value
        """
        if word not in self.operators:
            raise TypeError('Predicate operator must be one of {0}. Got {1}.'.format(self.operators, word))
        operator = None
        if word.lower() == 'equals' or word.lower() == 'eq' or word == '==':
            if b is None:
                operator = ' is '
            else:
                operator = '=='
        if word.lower() == 'gt':
            operator = '>'
        if word.lower() == 'gte':
            operator = '>='
        if word.lower() == 'lt':
            operator = '<'
        if word.lower() == 'lte':
            operator = '<='
        if word.lower() == 'ne' or word.lower() == '!=':
            if b is None:
                operator = ' is not '
            else:
                operator = '!='
        if word.lower() == 'in' or word.lower() == 'not in':
#             if not isinstance(b, (list, tuple)):
#                 raise TypeError('Invalid combination. Rule predicate expects [in, not in] when comparing to a list or tuple.')
            operator = word.lower()
        if not operator:
            raise TypeError('Unrecognized operator in rule predicate. Valid options are equals, eq, gt, gte, lt, lte, ne, in, not in. Options are not case sensitive')
        if a is None and word in ('equals', 'eq', 'ne', 'gt', 'gte', 'lt', 'lte'):
            try:
                # set a to 0 if b is an integer
                int(b)
                a = 0
            except:
                pass
        if (a is None or b is None) and word not in ('equals', 'eq', 'ne'):
            raise TypeError('Invalid predicate operator in rule for value None. Must be (equals, ea or ne). Got \'{0}\'.'.format(word))
        return operator

    @property
    def predicate_field_value(self):
        return self._predicate_field_value

    @predicate_field_value.setter
    def predicate_field_value(self, field_name):
        """ Returns a field value either by applying getattr to the source model or, if the field name matches one in RegisteredSubject, returns that value."""
        self._predicate_field_value = None
        if field_name == 'consent_version':
            self._predicate_field_value = ConsentHelper(self.visit_instance, suppress_exception=True).get_current_consent_version()
            if not self._predicate_field_value:
                self._predicate_field_value = 0
        elif field_name == 'hiv_status':
            self._predicate_field_value, is_default_value = site_lab_tracker.get_value(
                'HIV',
                self.visit_instance.get_subject_identifier(),
                self.visit_instance.get_subject_type(),
                self.visit_instance.report_datetime)
        else:
            self._predicate_field_value = getattr(self.source_instance, field_name)

        if self._predicate_field_value:
            if isinstance(self._predicate_field_value, basestring):
                self._predicate_field_value = re.escape(self._predicate_field_value).lower()
            else:
                field_inst = [fld for fld in self.source_instance._meta.fields if fld.name == field_name]
                if field_inst:
                    if isinstance(field_inst[0], IntegerField):
                        self._predicate_field_value = int(self._predicate_field_value)

    @property
    def predicate_comparative_value(self):
        return self._predicate_comparative_value

    @predicate_comparative_value.setter
    def predicate_comparative_value(self, value):
        self._predicate_comparative_value = value
        if self._predicate_comparative_value:
            if isinstance(self._predicate_comparative_value, basestring):
                self._predicate_comparative_value = re.escape(self._predicate_comparative_value).lower()

    @property
    def unresolved_predicate(self):
        return self._unresolved_predicate

    @unresolved_predicate.setter
    def unresolved_predicate(self, value):
        self._unresolved_predicate = value
        if not value:
            self._unresolved_predicate = self.logic.predicate
        else:
            self._unresolved_predicate = value
        if isinstance(self._unresolved_predicate[0], basestring):
            self._unresolved_predicate = (self._unresolved_predicate, )
        elif isinstance(self._unresolved_predicate[0], tuple):
            pass
        else:
            raise TypeError('First item in predicate must be a string or tuple of (field, operator, value).')
        if not isinstance(self._unresolved_predicate, tuple):
            raise TypeError('First \'logic\' item must be a tuple of (field, operator, value). Got %s' % (self._unresolved_predicate,))

    @property
    def predicate(self):
        """Converts the predicate to something like "value==value" that can be evaluated with eval().

        Return value may be '' or None, so users should check for this.

        A simple predicate would be a tuple ('field_name', 'equals', 'value') meant to resolve to 'value' == 'value'.
        A more complex one might be (('field_name', 'equals', 'value'), ('field_name', 'equals', 'value', 'or'))
        which would resolve to 'value' == 'value' or 'value' == 'value'.
        """
        self._predicate = None

        if self.source_instance:  # if no instance, just skip the rule
            self._predicate = ''
            self.unresolved_predicate = self.logic.predicate
            n = 0
            for item in self.unresolved_predicate:
                if n == 0 and not len(item) == 3:
                    raise ValueError('The logic tuple (or the first tuple of tuples) must must have three items. See {0}'.format(self))
                if n > 0 and not len(item) == 4:
                    raise ValueError('Additional tuples in the logic tuple must have a boolean operator as the fourth item. See {0}'.format(self))
                self.predicate_field_value = item[0]
                self.predicate_comparative_value = item[2]
                # logical_operator if more than one tuple in the logic tuple
                if len(item) == 4:
                    logical_operator = item[3]
                    if logical_operator not in ['and', 'or', 'and not', 'or not']:
                        raise ValueError('Invalid logical operator in logic tuple for rule {0}. Got {1}.'
                                   'Valid options are {2}'.format(self, logical_operator, ', '.join(['and', 'or', 'and not', 'or not'])))
                else:
                    logical_operator = ''
                if isinstance(self.predicate_comparative_value, list):
                    self.predicate_comparative_value = ';'.join([x.lower() for x in self.predicate_comparative_value])
                if self.predicate_comparative_value == 'None':
                    self.predicate_comparative_value = None
                # check type of field value and comparative value, must be the same or <Some>Type to NoneType
                # if a or b are string or None
                if (isinstance(self.predicate_field_value, (unicode, basestring)) or self.predicate_field_value is None) and (isinstance(self.predicate_comparative_value, (unicode, basestring)) or self.predicate_comparative_value is None):
                    predicate_template = ' {logical_operator} (\'{field_value}\' {operator} \'{comparative_value}\')'
                    self._predicate = self._predicate.replace('\'None\'', 'None')
                # if a or b are number or None
                elif (isinstance(self.predicate_field_value, (int, long, float)) or self.predicate_field_value is None) and (isinstance(self.predicate_comparative_value, (int, long, float)) or self.predicate_comparative_value is None):
                    predicate_template = ' {logical_operator} ({field_value} {operator} {comparative_value})'
                # if a is a date and b is a date, datetime
                elif isinstance(self.predicate_field_value, (date)) and isinstance(self.predicate_comparative_value, (date, datetime)):
                    if isinstance(self.predicate_comparative_value, datetime):
                        # convert b to date to match type of a
                        self.predicate_comparative_value = date(date.year, date.month, date.day)
                    predicate_template = ' {logical_operator} (datetime.strptime({field_value},\'%Y-%m-%d\') {operator} datetime.strptime({comparative_value},\'%Y-%m-%d\'))'
                # if a is a datetime and b is a date, datetime
                elif isinstance(self.predicate_field_value, (datetime)) and isinstance(self.predicate_comparative_value, (date, datetime)):
                    if isinstance(self.predicate_comparative_value, date):
                        # convert a to date if b is a date
                        self.predicate_field_value = date(date.year, date.month, date.day)
                    predicate_template = ' {logical_operator} (datetime.strptime({field_value},\'%Y-%m-%d %H:%M\') {operator} datetime.strptime({comparative_value},\'%Y-%m-%d %H:%M\'))'
                else:
                    if isinstance(self.predicate_field_value, (date, datetime)) and self.predicate_comparative_value is None:
                        raise TypeError('In a rule predicate, may not compare a date or datetime to None. Got \'{0}\' and \'{1}\''.format(self.predicate_field_value, self.predicate_comparative_value))
                    else:
                        pass
                        #raise TypeError('Rule predicate values must be of the same data type and be either strings, dates or numbers. Got \'{0}\' and \'{1}\''.format(self.predicate_field_value, self.predicate_comparative_value))
                self._predicate += predicate_template.format(
                       logical_operator=logical_operator,
                       field_value=self.predicate_field_value,
                       operator=self.get_operator_from_word(item[1], self.predicate_field_value, self.predicate_comparative_value),
                       comparative_value=self.predicate_comparative_value)
                n += 1
        return self._predicate

    @property
    def target_model(self):
        return self._target_model

    @target_model.setter
    def target_model(self, target_model):
        """Sets a list of target models.

        Target models are the models for whose meta data is affected by the rule.

        Target models always have an attribute pointing to the visit instance."""
        self._target_model = target_model
        if isinstance(self._target_model, basestring):
            self._target_model = get_model(self.app_label, self._target_model)
        if not self._target_model:
            raise AttributeError('Target model may not be None.')

    @property
    def visit_instance(self):
        return self._visit_instance

    @visit_instance.setter
    def visit_instance(self, visit_instance):
        if not isinstance(visit_instance, BaseVisitTracking):
            raise TypeError('Parameter \'visit_instance\' must be an instance of BaseVisitTracking.')
        self._visit_instance = visit_instance

    @property
    def source_instance(self):
        """ Sets the source model instance.

        Source model may be any model with a FK to the visit_instance, any model with a FK to registered_subject,
        or registered_subject itself.

        If the source model instance does not exist (yet), value is None"""
        if not self._source_instance:
            if self.source_model._meta.object_name.lower() == 'registeredsubject':
                self._source_instance = self.visit_instance.appointment.registered_subject
            elif [fld.name for fld in self.source_model._meta.fields if fld.name == 'registered_subject']:
                self._source_instance = self.source_model.objects.get(registered_subject=self.visit_instance.appointment.registered_subject)
            else:
                if self.source_model.objects.filter(**{self.visit_attr_name: self.visit_instance}).exists():
                    self._source_instance = self.source_model.objects.get(**{self.visit_attr_name: self.visit_instance})
        return self._source_instance
