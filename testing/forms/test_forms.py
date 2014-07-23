from base.form.forms import BaseModelForm
from ..models import TestModel, TestSubjectUuidModel, TestScheduledModel


class TestSubjectUuidModelForm (BaseModelForm):

    class Meta:
        model = TestSubjectUuidModel


class TestModelForm (BaseModelForm):

    class Meta:
        model = TestModel


class TestScheduledModelForm(BaseModelForm):
    class Meta:
        model = TestScheduledModel
