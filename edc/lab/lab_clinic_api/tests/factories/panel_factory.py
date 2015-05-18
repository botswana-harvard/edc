import factory

from lis.specimen.lab_panel.tests.factories import BasePanelFactory

from ...models import Panel


class PanelFactory(BasePanelFactory):
    FACTORY_FOR = Panel

    panel_type = factory.Sequence(lambda n: 'TEST{0}'.format(n))
