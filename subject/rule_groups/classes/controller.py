import copy

from collections import OrderedDict

from django.conf import settings
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

from edc.subject.entry.models import Entry

from .rule_group import RuleGroup


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class Controller(object):

    """ Main controller of :class:`RuleGroup` objects. """

    def __init__(self):
        self._registry = OrderedDict()  # ordered to ensure rules fire in the same order as listed in the source module.

    def set_registry(self, rule_group):
        if not issubclass(rule_group, RuleGroup):
            raise AlreadyRegistered('Expected an instance of RuleGroup.')
        if not rule_group.app_label in self._registry:
            self._registry.update({rule_group.app_label: []})
        if rule_group in self._registry.get(rule_group.app_label):
            raise AlreadyRegistered('The rule {0} is already registered for module {1}'.format(rule_group.__name__, rule_group.app_label))
        self._registry.get(rule_group.app_label).append(rule_group)

    def get_registry(self, app_label=None):
        """Returns the an ordered dictionary of rules for the app_label."""
        if app_label:
            if app_label in self._registry:
                return self._registry.get(app_label)
            else:
                return {}
        return self._registry

    def register(self, rule_group):
        """ Register Rule groups to the list for the module the rule groups were declared in; which is the same module as the visit model (see update)."""
        self.set_registry(rule_group)

    def update_all(self, visit_model_instance):
        """ Given a visit model instance, run all rules in each rule group for the app_label of the visit model."""
        app_label = visit_model_instance._meta.app_label
        for rule_group in self.get_registry(app_label):
            for rule in rule_group.rules:
                rule.run(visit_model_instance)

    def update_for_visit_definition(self, visit_instance):
        """ Given a visit model instance, run all rules in the rule group module for the visit definition in order of the entries (rule source model)."""
        for entry in Entry.objects.filter(visit_definition__code=visit_instance.appointment.visit_definition.code).order_by('entry_order'):
            source_model = entry.get_model()
            for rule in self.get_rules_for_source_model(source_model):
                rule.run(visit_instance)

    def update_rules_for_source_model(self, source_model, visit_instance):
        for rule in self.get_rules_for_source_model(source_model):
            rule.run(visit_instance)

    def get_rules_for_source_model(self, source_model):
        """Returns a list of rules filtered on source_model.

        Takes a list of rules for app_label=<source_model.app_label> and filters on source_model=<source_model>.

        ..note:: if RuleGroup attribute Meta.source_model=None, source_model will default to RegisteredSubject."""
        filtered_list_of_rules = []
        registeredsubject_list_of_rules = []
        for rule_group in self.get_registry(source_model._meta.app_label):
            for rule in rule_group.rules:
                if rule.source_model._meta.object_name.lower() == 'registeredsubject':
                    registeredsubject_list_of_rules.append(rule)
                if rule.source_model == source_model:
                    filtered_list_of_rules.append(rule)
        return registeredsubject_list_of_rules + filtered_list_of_rules

    def autodiscover(self):
        """ Autodiscover rules from a rule_groups module."""
        for app in settings.INSTALLED_APPS:
            mod = import_module(app)
            try:
                before_import_registry = copy.copy(site_rule_groups._registry)
                import_module('%s.rule_groups' % app)
            except:
                site_rule_groups._registry = before_import_registry
                if module_has_submodule(mod, 'rule_groups'):
                    raise

site_rule_groups = Controller()
