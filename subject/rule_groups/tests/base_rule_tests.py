from django.test import TestCase

from edc.subject.entry.models import ScheduledEntryMetaData
from edc.subject.entry.classes import ScheduledEntry

from ..classes import BaseRule, Logic


class BaseRuleTests(TestCase):

    def test_get_operator_from_word(self):
        base_rule = BaseRule()
        self.assertRaises(TypeError, base_rule.get_operator_from_word, 'nathan', 1, [1, 2])
        self.assertEqual(base_rule.get_operator_from_word('eq', 1, 1), '==')
        self.assertEqual(base_rule.get_operator_from_word('==', 1, 1), '==')
        self.assertEqual(base_rule.get_operator_from_word('lt', 1, 1), '<')
        self.assertEqual(base_rule.get_operator_from_word('lte', 1, 1), '<=')
        self.assertEqual(base_rule.get_operator_from_word('gt', 1, 1), '>')
        self.assertEqual(base_rule.get_operator_from_word('gte', 1, 1), '>=')
        self.assertEqual(base_rule.get_operator_from_word('lt', 1, 1), '<')
        self.assertEqual(base_rule.get_operator_from_word('lte', 1, 1), '<=')
        self.assertEqual(base_rule.get_operator_from_word('ne', 1, 1), '!=')
        self.assertEqual(base_rule.get_operator_from_word('!=', 1, 1), '!=')
        self.assertEqual(base_rule.get_operator_from_word('in', 1, [1, 2]), 'in')
        self.assertEqual(base_rule.get_operator_from_word('not in', 1, [1, 2]), 'not in')

    def rule_can_initialize(self):

        class TestRule(BaseRule):

            def set_entry_class(self):
                self._entry_class = ScheduledEntry

            def set_meta_data_model(self):
                self._meta_data_model = ScheduledEntryMetaData

            def get_action_list(self):
                return ['new', 'not_required']

        test_rule = TestRule(
            logic=Logic(
                predicate=(('f4', 'equals', 'No')),
                consequence='not_required',
                alternative='new'),
            target_model=['testscheduledmodel'])

