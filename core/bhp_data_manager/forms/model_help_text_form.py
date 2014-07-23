from django import forms
from django.db.models import get_model
from base.form.forms import BaseModelForm
from ..models import ModelHelpText


class ModelHelpTextForm(BaseModelForm):

    def clean(self):

        cleaned_data = self.cleaned_data
        model = get_model(cleaned_data.get('app_label', None), cleaned_data.get('module_name', None))
        if not model:
            raise forms.ValidationError('app_label and/or module name are invalid')
        return cleaned_data

    class Meta:
        model = ModelHelpText
