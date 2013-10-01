from django.test import TestCase
from edc.subject.registration.tests.factories import RegisteredSubjectFactory
from edc.subject.lab_tracker.classes import site_lab_tracker
from .factories import AliquotFactory, AliquotConditionFactory, ReceiveFactory, OrderFactory, ResultFactory, ResultItemFactory


class TestModelMethods(TestCase):

    def test_order(self):
        site_lab_tracker.autodiscover()
        registered_subject = RegisteredSubjectFactory()
        receive = ReceiveFactory(registered_subject=registered_subject)
        aliquot_condition = AliquotConditionFactory(short_name='10')
        aliquot = AliquotFactory(receive=receive, aliquot_condition=aliquot_condition)
        order = OrderFactory(aliquot=aliquot)
        result = ResultFactory(order=order)
        result_item = ResultItemFactory(result=result)
