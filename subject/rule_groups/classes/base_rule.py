import re

from datetime import date, datetime

from django.db.models import get_model, Model, IntegerField
from django.core.exceptions import ImproperlyConfigured

from edc.subject.consent.classes import ConsentHelper
from edc.subject.entry.classes import BaseEntry
from edc.subject.entry.models import BaseEntryMetaData
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.registration.models import RegisteredSubject
from edc.subject.visit_tracking.models import BaseVisitTracking

from .logic import Logic


class BaseRule(object):
    """Base class for all rules."""

    OPERATORS = ['equals', 'eq', 'gt', 'gte', 'lt', 'lte', 'ne', '!=', '==', 'in', 'not in']

    def __init__(self, *args, **kwargs):

        self._site_lab_tracker = None
        self._predicate = None
        self._consequent_action = None
        self._alternative_action = None
        self._comment = None
        self._target_model_list = None
        self._target_model = None
        self._source_model = None
        self._filter_fieldname = None
        self._filter_instance = None
        self._filter_model_cls = None
        self._source_instance = None
        self._meta_data_model = None
        self._entry_class = None
        self._meta_data_instance = None
        self._target_content_type_map = None
        self._visit_model_instance = None
        self.rule_group_name = ''

        if 'logic' in kwargs:
            self.set_logic(kwargs.get('logic'))
        if 'target_model' in kwargs:
            self.set_target_model_list(kwargs.get('target_model'))
        # these attributes usually come in thru Meta, but not always...
        if 'source_model' in kwargs:
            self.set_source_model(kwargs.get('source_model'))
            # set attribute for inspection by RuleGroup
            self.source_model = kwargs.get('source_model')
        if 'filter_model' in kwargs:
            self.set_filter_model_cls(kwargs.get('filter_model')[0])
            self.set_filter_fieldname(kwargs.get('filter_model')[1])
            # set attribute for inspection by RuleGroup
            self.filter_model = kwargs.get('filter_model')
        self._set_meta_data_model()
        self.set_entry_class()

    def __repr__(self):
        return '{0}.{1}'.format(self.rule_group_name, self.name)

    def reset(self, visit_model_instance=None):
        """ Resets before run()."""
        self._source_instance = None
        self._meta_data_instance = None
#         self._target_content_type_map = None
        self.set_visit_model_instance(visit_model_instance)
        self.set_filter_instance()
        self.set_meta_data_instance()

    def run(self, visit_model_instance):
        """ Evaluate the rule for each target model in the target model list."""
        for target_model in self.get_target_model_list():
            self.set_target_model(target_model)
            self.reset(visit_model_instance)
            self.evaluate()

    def evaluate(self):
        raise AttributeError('Evaluate should be overridden. Nothing to do.')

    def get_site_lab_tracker(self):
        return site_lab_tracker

    def set_logic(self, logic):
        if isinstance(logic, Logic):
            self._logic = logic
            if self._logic is None:
                raise AttributeError('Logic cannot be None.')
            if self.is_valid_action(logic.consequence):
                self.set_consequent_action(logic.consequence)
            if self.is_valid_action(logic.alternative):
                self.set_alternative_action(logic.alternative)
            if 'comment' in dir(logic):
                self.set_comment(logic.comment)
        else:
            raise AttributeError('Attribute \'logic\' must be an instance of class Logic.')

    def get_logic(self):
        return self._logic

    def set_consequent_action(self, action):
        self._consequent_action = action

    def get_consequent_action(self):
        return self._consequent_action

    def set_alternative_action(self, action):
        self._alternative_action = action

    def get_alternative_action(self):
        return self._alternative_action

    def set_comment(self, value):
        self._comment = value

    def get_comment(self):
        return self._comment

    def get_action_list(self):
        """Users should override to return a valid list of actions for consequent and alternative actions.

        For example ['new', 'not_required']."""
        raise TypeError('Action list cannot be None.')

    def is_valid_action(self, action):
        """Returns true if the action is in the list of valid actions or, if invalid action, raises an error."""
        if action.lower() not in self.get_action_list():
            raise TypeError('Encountered an invalid action \'{0}\' when parsing additional rule. '
                            'Valid actions are {1}.'.format(action, ', '.join(self.get_action_list())))
        return True

    def get_operator_from_word(self, word, a, b):
        """Returns the operator from the 'word' used in the predicate, for example 'equals' returns '=='.

            Args:
                a = field_value
                b = comparative_value
        """
        if word not in self.OPERATORS:
            raise TypeError('Predicate operator must be one of {0}. Got {1}.'.format(self.OPERATORS, word))
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
            if not isinstance(b, (list, tuple)):
                raise TypeError('Invalid combination. Rule predicate expects [in, not in] when comparing to a list or tuple.')
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

    def _set_predicate_field_value(self, instance, field_name):
        """ Returns a field value either by applying getattr to the source model or, if the field name matches one in RegisteredSubject, returns that value.

        Some RegisteredSubject field names are excluded:
            ['id', 'created', 'modified', 'hostname_created', 'hostname_modified', 'study_site', 'survival_status', 'hiv_status']"""
        registered_subject_override_field_names = ['id', 'created', 'modified', 'hostname_created', 'hostname_modified', 'study_site', 'survival_status', 'hiv_status']
        if field_name in [field.name for field in RegisteredSubject._meta.fields if field.name not in registered_subject_override_field_names]:
            registered_subject = self.get_visit_model_instance().appointment.registered_subject
            self._field_value = getattr(registered_subject, field_name)
        elif field_name == 'consent_version':
            self._field_value = ConsentHelper(self.get_visit_model_instance(), suppress_exception=True).get_current_consent_version()
            if not self._field_value:
                self._field_value = 0
        elif field_name == 'hiv_status':
            self._field_value, is_default_value = self.get_site_lab_tracker().get_value('HIV', self.get_visit_model_instance().get_subject_identifier(), self.get_visit_model_instance().get_subject_type(), self.get_visit_model_instance().report_datetime)
        else:
            self._field_value = getattr(instance, field_name)
        if self._field_value:
            if isinstance(self._field_value, basestring):
                self._field_value = re.escape(self._field_value).lower()
            else:
                field_inst = [fld for fld in instance._meta.fields if fld.name == field_name]
                if field_inst:
                    if isinstance(field_inst[0], IntegerField):
                        # make sure is int and not long
                        self._field_value = int(self._field_value)

    def _get_predicate_field_value(self):
        return self._field_value

    def _set_predicate_comparative_value(self, value):
        self._comparative_value = value
        if self._comparative_value:
            if isinstance(self._comparative_value, basestring):
                self._comparative_value = re.escape(self._comparative_value).lower()

    def _get_predicate_comparative_value(self):
        return self._comparative_value

    def _set_unresolved_predicate(self, value=None):
        if not value:
            self._unresolved_predicate = self.get_logic().predicate
        else:
            unresolved_predicate = value
            if isinstance(unresolved_predicate[0], basestring):
                unresolved_predicate = (unresolved_predicate,)
            elif isinstance(unresolved_predicate[0], tuple):
                unresolved_predicate = unresolved_predicate
            else:
                raise TypeError('First item in predicate must be a string or tuple of (field, operator, value).')
            # build the predicate
            # check that unresolved predicate is a tuple
            if not isinstance(unresolved_predicate, tuple):
                raise TypeError('First \'logic\' item must be a tuple of (field, operator, value). Got %s' % (unresolved_predicate,))
            self._unresolved_predicate = unresolved_predicate

    def _get_unresolved_predicate(self):
        return self._unresolved_predicate

    def set_predicate(self):
        """Converts the predicate to something like "value==value" that can be evaluated with eval().

        A simple predicate would be a tuple ('field_name', 'equals', 'value') meant to resolve to 'value' == 'value'.
        A more complex one might be (('field_name', 'equals', 'value'), ('field_name', 'equals', 'value', 'or'))
        which would resolve to 'value' == 'value' or 'value' == 'value'.
        """
        self._predicate = None
        if self.get_source_instance():  # if no instance, just skip the rule
            self._predicate = ''
            self._set_unresolved_predicate(self.get_logic().predicate)
            n = 0
            for item in self._get_unresolved_predicate():
                if n == 0 and not len(item) == 3:
                    ValueError('The logic tuple (or the first tuple of tuples) must must have three items')
                if n > 0 and not len(item) == 4:
                    ValueError('Additional tuples in the logic tuple must have a boolean operator as the fourth item')
                self._set_predicate_field_value(self.get_source_instance(), item[0])
                self._set_predicate_comparative_value(item[2])
                # logical_operator if more than one tuple in the logic tuple
                if len(item) == 4:
                    logical_operator = item[3]
                    if logical_operator not in ['and', 'or', 'and not', 'or not']:
                        ValueError('Invalid logical operator in logic tuple for rule {0}. Got {1}. '
                                   'Valid options are {2}'.format(self, logical_operator, ', '.join(['and', 'or', 'and not', 'or not'])))
                else:
                    logical_operator = ''
                # add as string for eval()
                a = self._get_predicate_field_value()
                b = self._get_predicate_comparative_value()
                if b == 'None':
                    b = None
                # check type of field value and comparative value, must be the same or <Some>Type to NoneType
                # if a or b are string or None
                if (isinstance(a, (unicode, basestring)) or a is None) and (isinstance(b, (unicode, basestring)) or b is None):
                    predicate_template = ' {logical_operator} (\'{field_value}\' {operator} \'{comparative_value}\')'
                    self._predicate = self._predicate.replace('\'None\'', 'None')
                # if a or b are number or None
                elif (isinstance(a, (int, long, float)) or a is None) and (isinstance(b, (int, long, float)) or b is None):
                    predicate_template = ' {logical_operator} ({field_value} {operator} {comparative_value})'
                # if a is a date and b is a date, datetime
                elif isinstance(a, (date)) and isinstance(b, (date, datetime)):
                    if isinstance(b, datetime):
                        # convert b to date to match type of a
                        b = date(date.year, date.month, date.day)
                    predicate_template = ' {logical_operator} (datetime.strptime({field_value},\'%Y-%m-%d\') {operator} datetime.strptime({comparative_value},\'%Y-%m-%d\'))'
                # if a is a datetime and b is a date, datetime
                elif isinstance(a, (datetime)) and isinstance(b, (date, datetime)):
                    if isinstance(b, date):
                        # convert a to date if b is a date
                        a = date(date.year, date.month, date.day)
                    predicate_template = ' {logical_operator} (datetime.strptime({field_value},\'%Y-%m-%d %H:%M\') {operator} datetime.strptime({comparative_value},\'%Y-%m-%d %H:%M\'))'
                else:
                    if isinstance(a, (date, datetime)) and b is None:
                        raise TypeError('In a rule predicate, may not compare a date or datetime to None. Got \'{0}\' and \'{1}\''.format(a, b))
                    else:
                        raise TypeError('Rule predicate values must be of the same data type and be either strings, dates or numbers. Got \'{0}\' and \'{1}\''.format(a, b))
                self._predicate += predicate_template.format(
                       logical_operator=logical_operator,
                       field_value=a,
                       operator=self.get_operator_from_word(item[1], a, b),
                       comparative_value=b)
                n += 1

    def get_predicate(self):
        """Gets the predicate, but return value may be '' or None, so users should check for this."""
        # always set
        self.set_predicate()
        return self._predicate

    def set_target_model_list(self, target_model_list=None):
        """ Sets up the target model list for this rule by converting model names to classes. """
        self._target_model_list = []
        # for each target model tuple, get the actual model
        # and append to the internal list of target models to run against
        for target_model in target_model_list:
            if isinstance(target_model, tuple):
                self._target_model_list.append(get_model(target_model[0], target_model[1]))
            else:
                # oh, app_label is in Meta ...
                # we'll have to convert to classes later in RuleGroup __metaclass__
                # just store the model_name as a string for now
                self._target_model_list.append(target_model)

    def get_target_model_list(self):
        return self._target_model_list

    def set_target_model(self, target_model=None):
        """Sets a list of target models.

        Target models are the models affected by the rule. For example, the entry status
        on the meta data instance for the target model will be NOT_REQUIRED. """
        if not target_model:
            raise AttributeError('Attribute _target_model cannot be None.')
        if not issubclass(target_model, Model):
            # could be that something went wrong when converting from model_name to model class in RuleGroup __metaclass__
            raise AttributeError('Attribute _target_model must be a Model Class. Got {0}'.format(target_model))
        self._target_model = target_model
        self._meta_data_instance = None

    def get_target_model(self):
        return self._target_model

    def set_source_model(self, model_cls=None):
        """Sets the source model class.

        The predicate refers to an attribute of the source model class."""
        self._source_instance = None
        if model_cls:
            if isinstance(model_cls, tuple):
                self._source_model = get_model(model_cls[0], model_cls[1])
            else:
                self._source_model = model_cls
        else:
            raise AttributeError('Attribute _source_model cannot be None.')

    def get_source_model(self):
        return self._source_model

    def set_visit_model_instance(self, visit_model_instance=None):
        if not isinstance(visit_model_instance, BaseVisitTracking):
            raise TypeError('Parameter \'visit_model_instance\' must be an instance of BaseVisitTracking.')
        self._visit_model_instance = visit_model_instance
        if not self._visit_model_instance:
            raise AttributeError('Attribute _visit_model_instance cannot be None')

    def get_visit_model_instance(self):
        return self._visit_model_instance

    def set_filter_fieldname(self, filter_fieldname=None):
        """Sets the filter fieldname that is used to filter on the source_model if a source_instance is not provided."""
        self._filter_fieldname = None
        if filter_fieldname:
            self._filter_fieldname = filter_fieldname
        else:
            raise AttributeError('Attribute _filter_fieldname cannot be None')

    def get_filter_fieldname(self):
        return self._filter_fieldname

    def set_filter_model_cls(self, model_cls=None):
        self._filter_instance = None
        if model_cls:
            if isinstance(model_cls, tuple):
                self._filter_model_cls = get_model(model_cls[0], model_cls[1])
            else:
                self._filter_model_cls = model_cls
        else:
            raise AttributeError('Attribute _filter_model_cls cannot be None.')

    def get_filter_model_cls(self):
        return self._filter_model_cls

    def set_filter_instance(self):
        """Sets the instance to filter the user model, for example an instance of a visit model or registered subject."""
        self._filter_instance = None
        if self.get_visit_model_instance():
            if self.get_filter_model_cls() == RegisteredSubject:
                self._filter_instance = self.get_visit_model_instance().appointment.registered_subject
            else:
                self._filter_instance = self.get_visit_model_instance()
        if not self._filter_instance:
            raise AttributeError('Attribute _filter_instance cannot be None')

    def get_filter_instance(self):
        return self._filter_instance

    def set_source_instance(self, source_instance=None):
        """ Set the user model instance using either a given instance or by filtering on the user model class.

        If the source model instance does not exist (yet), value is None"""
        self._source_instance = None
        if source_instance:
            self._source_instance = source_instance
        elif self.get_source_model()._meta.object_name.lower() == 'registeredsubject':
            # special case
            self._source_instance = self.get_visit_model_instance().appointment.registered_subject
        else:
            if self.get_source_model().objects.filter(**{self.get_filter_fieldname(): self.get_filter_instance()}).exists():
                self._source_instance = self.get_source_model().objects.get(**{self.get_filter_fieldname(): self.get_filter_instance()})

    def get_source_instance(self):
        """Gets the source model instance but users should check if the return value is None."""
        return self._source_instance

    def _set_meta_data_model(self):
        """Sets the entry bucket class but users should override"""
        self.set_meta_data_model()
        if not self._meta_data_model:
            raise AttributeError('Attribute _meta_data_model cannot be None')
        if not issubclass(self._meta_data_model, BaseEntryMetaData):
            raise AttributeError('Attribute _meta_data_model must be a subclass of BaseEntryMetaData.')

    def set_meta_data_model(self):
        raise ImproperlyConfigured('You have to override this method in the child class to set the instance attribute _meta_data_model.')

    def get_meta_data_model(self):
        return self._meta_data_model

    def _set_entry_class(self):
        """Sets the entry class but users should override."""
        self.set_entry_class()
        if not self._entry_class:
            raise AttributeError('Attribute _entry_class cannot be None')
        if not issubclass(self._entry_class, BaseEntry):
            raise AttributeError('Attribute _entry_class must be a subclass of BaseEntry.')

    def set_entry_class(self):
        raise ImproperlyConfigured('You have to override this method in the child class to set the instance attribute entry_class.')

    def get_entry_class(self):
        return self._entry_class

    def set_meta_data_instance(self, meta_data_model):
        """Users should override"""
        self._meta_data_instance = None
        if not self._meta_data_instance:
            raise AttributeError('Attribute _meta_data_instance cannot be None')

    def get_meta_data_instance(self):
        return self._meta_data_instance

#     def set_target_content_type_map(self):
#         """Sets the content type for the target model to help locate the target's entry bucket instance."""
#         self._target_content_type_map = ContentTypeMap.objects.get(
#             app_label=self.get_target_model()._meta.app_label,
#             model=self.get_target_model()._meta.object_name.lower())
# 
#     def get_target_content_type_map(self):
#         return self._target_content_type_map
