import factory

from ...models import TestSubjectUuidModel


class TestSubjectUuidModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = TestSubjectUuidModel
