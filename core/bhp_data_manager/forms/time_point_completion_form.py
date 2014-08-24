from django import forms
from edc.base.form.forms import BaseModelForm
from ..models import TimePointCompletion


class TimePointCompletionForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(TimePointCompletionForm, self).clean()
        if cleaned_data.get('status') == 'feedback' and not cleaned_data.get('comment'):
            raise forms.ValidationError('If feedback is being given, please provide a fully detailed description in the comment box below')

        if cleaned_data.get('subject_withdrew') == 'Yes' and cleaned_data.get('reasons_withdrawn') == 'N/A':
            raise forms.ValidationError('If subject is withdrawing, REASON for withdrawal cannot be NOT APPLICABLE')

        if cleaned_data.get('subject_withdrew') == 'Yes' and not cleaned_data.get('date_withdrawn'):
            raise forms.ValidationError('If subject is withdrawing, please provide date of withdrawal')

        if cleaned_data.get('subject_withdrew') == 'Yes' and cleaned_data.get('date_withdrawn'):
            from apps.bcpp_subject.models import SubjectConsent
            consent = SubjectConsent.objects.get(registered_subject__subject_identifier=cleaned_data.get('registered_subject').subject_identifier)
            if consent:
                if cleaned_data.get('date_withdrawn', None) != consent.consent_datetime:
                    raise forms.ValidationError('the consent withdrawal date IS NOT EQUAL to the consent date. Got {0} != {1}'.format(cleaned_data.get('date_withdrawn'), consent.consent_datetime))

        return cleaned_data

    class Meta:
        model = TimePointCompletion
