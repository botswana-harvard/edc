from django.db.models import get_model

from .base_rule import BaseRule


class BaseRuleGroup(type):

    app_label = None
    source_model = None
    filter_model = None

    def __new__(cls, name, bases, attrs):
        """Add the Meta attributes to each rule."""
        rules = []
        parents = [b for b in bases if isinstance(b, BaseRuleGroup)]
        if not parents:
            # If this isn't a subclass of BaseRuleGroup, don't do anything special.
            return super(BaseRuleGroup, cls).__new__(cls, name, bases, attrs)
        meta = attrs.pop('Meta', None)
        # source model is the same for all rules in this group, so get it now
        if isinstance(meta.source_model, tuple):
            source_model = get_model(meta.source_model[0], meta.source_model[1])
        else:
            source_model = meta.source_model
        # source fk model and attr are the same for all rules in this group, so get it now
        if not meta.source_fk:
            source_fk_model = None
            source_fk_attr = None
        else:
            if isinstance(meta.source_fk[0], tuple):
                source_fk_model = get_model(meta.source_fk[0][0], meta.source_model[0][1])
            else:
                source_fk_model = meta.source_fk[0]
            source_fk_attr = meta.source_fk[1]
        for rule_name, rule in attrs.items():
            if not rule_name.startswith('_'):
                if isinstance(rule, BaseRule):
                    rule.name = '{0}.{1}'.format(name, rule_name)
                    if meta:
                        rule.app_label = meta.app_label
                        for item in rule.target_model_list:
                            if isinstance(item, basestring):
                                rule.target_model_names.append(item)
                                model_name = rule.target_model_list.pop(rule.target_model_list.index(item))
                                model_cls = get_model(meta.app_label, model_name)
                                if not model_cls:
                                    raise AttributeError('Attribute \'target_model\' in rule \'{0}.{1}\' contains a model_name that does not exist. app_label=\'{2}\', model_name=\'{3}\'.'.format(name, rule_name, meta.app_label, model_name))
                                rule.target_model_list.append(model_cls)
                        rule.source_model = source_model
                        rule.source_fk_model = source_fk_model
                        rule.source_fk_attr = source_fk_attr
                    rules.append(rule)
                    attrs.update({rule_name: rule})
        attrs.update({'rules': tuple(rules)})
        attrs.update({'app_label': meta.app_label})
        attrs.update({'source_model': source_model})
        attrs.update({'source_fk_model': source_fk_model})
        attrs.update({'source_fk_attr': source_fk_attr})
        attrs.update({'_meta': meta})
        attrs.update({'name': name})
        return super(BaseRuleGroup, cls).__new__(cls, name, bases, attrs)


class RuleGroup(object):

    """ All rule groups inherit from this.

    RuleGroups are contained by the Controller
    """
    __metaclass__ = BaseRuleGroup

    def __repr__(self):
        return self.name

    def run_all(self, visit_model_instance):
        for rule in self.rules:
            rule.run(visit_model_instance)
