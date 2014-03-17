import factory

from edc.lab.lab_requisition.tests.factories import BaseRequisitionFactory

from ...models import TestRequisition

from .test_visit_factory import TestVisitFactory
#from .test_panel_factory import TestPanelFactory
#from .test_aliquot_type_factory import TestAliquotTypeFactory


class TestRequisitionFactory(BaseRequisitionFactory):
    FACTORY_FOR = TestRequisition

    test_visit = factory.SubFactory(TestVisitFactory)
#    panel = factory.SubFactory(TestPanelFactory)
#   aliquot_type = factory.SubFactory(TestAliquotTypeFactory)
