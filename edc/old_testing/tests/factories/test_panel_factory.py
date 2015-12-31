import factory


from ...models import TestPanel


class TestPanelFactory(factory.DjangoModelFactory):
    class Meta:
        model = TestPanel

    name = factory.Sequence(lambda n: 'Panel {0}'.format(n))
