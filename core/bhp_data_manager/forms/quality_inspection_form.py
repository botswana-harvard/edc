from django import forms
from edc.base.form.forms import BaseModelForm
from ..models import QualityInspection


class QualityInspectionForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(QualityInspectionForm, self).clean()
        if cleaned_data.get('status') == 'feedback' and not cleaned_data.get('comment'):
            raise forms.ValidationError('If feedback is being given, please provide a fully detailed description in the comment box below')
        return cleaned_data

    class Meta:
        model = QualityInspection
