import factory

from ...models import TestModel


class TestModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = TestModel

    f1 = factory.Sequence(lambda n: 'F1{0}'.format(n))
    f2 = factory.Sequence(lambda n: 'F2{0}'.format(n))
    f3 = factory.Sequence(lambda n: 'F3{0}'.format(n))
    f4 = factory.Sequence(lambda n: 'F4{0}'.format(n))
    f5 = factory.Sequence(lambda n: 'F5{0}'.format(n))
