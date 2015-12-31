from django import forms

from ..models import TestModel, TestSubjectUuidModel, TestScheduledModel


class TestSubjectUuidModelForm (forms.ModelForm):

    class Meta:
        model = TestSubjectUuidModel


class TestModelForm (forms.ModelForm):

    class Meta:
        model = TestModel


class TestScheduledModelForm(forms.ModelForm):
    class Meta:
        model = TestScheduledModel
