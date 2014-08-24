from django import forms
from edc.base.form.forms import BaseModelForm
from ..models import TimePointCompletion


class TimePointCompletionForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(TimePointCompletionForm, self).clean()
        if cleaned_data.get('status') == 'feedback' and not cleaned_data.get('comment'):
            raise forms.ValidationError('If feedback is being given, please provide a fully detailed description in the comment box below')

        if cleaned_data.get('subject_withdrew') == 'Yes' and not cleaned_data.get('reasons_withdrawn'):
            raise forms.ValidationError('If subject is withdrawing, what are the reasons for withdrawal?')

        if cleaned_data.get('subject_withdrew') == 'Yes' and not cleaned_data.get('date_withdrawn'):
            raise forms.ValidationError('If subject is withdrawing, please provide date of withdrawal')

        return cleaned_data

    class Meta:
        model = TimePointCompletion
