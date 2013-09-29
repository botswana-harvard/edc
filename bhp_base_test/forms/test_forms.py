from edc_core.bhp_base_form.forms import BaseModelForm
from ..models import TestModel, TestSubjectUuidModel


class TestSubjectUuidModelForm (BaseModelForm):

    class Meta:
        model = TestSubjectUuidModel


class TestModelForm (BaseModelForm):

    class Meta:
        model = TestModel
