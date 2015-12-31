import factory

from django.utils import timezone

from ...models import TestSubjectResultModel


class TestSubjectResultModelFactory(factory.DjangoModelFactory):
    class Meta:
        model = TestSubjectResultModel

    result_datetime = timezone.now()
