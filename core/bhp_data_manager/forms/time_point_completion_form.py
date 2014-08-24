from django import forms

from edc.base.form.forms import BaseModelForm

from ..models import TimePointCompletion


class TimePointCompletionForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(TimePointCompletionForm, self).clean()
        self.instance.check_time_point_completion(forms.ValidationError)
        if cleaned_data.get('status') == 'feedback' and not cleaned_data.get('comment'):
            raise forms.ValidationError('If feedback is being given, please provide a fully detailed description in the comment box below')

        if cleaned_data.get('subject_withdrew') == 'Yes' and cleaned_data.get('reasons_withdrawn') == 'N/A':
            raise forms.ValidationError('If subject is withdrawing, REASON for withdrawal cannot be NOT APPLICABLE')

        if cleaned_data.get('subject_withdrew') == 'Yes' and not cleaned_data.get('date_withdrawn'):
            raise forms.ValidationError('If subject is withdrawing, please provide date of withdrawal')

        self.instance.validate_status(forms.ValidationError)
        return cleaned_data

    class Meta:
        model = TimePointCompletion
