from edc.lab.lab_panel.tests.factories import BasePanelFactory
from ...models import Panel


class PanelFactory(BasePanelFactory):
    FACTORY_FOR = Panel

    panel_type = 'TEST'
    # m2m aliquot_type = factory.SubFactory(AliquotTypeFactory)
