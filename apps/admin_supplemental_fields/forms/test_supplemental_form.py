from django import forms

from ..models import TestSupplemental


class TestSupplementalForm(forms.ModelForm):

    class Meta:
        model = TestSupplemental
