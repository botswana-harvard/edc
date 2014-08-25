from django.forms import ValidationError

from edc.base.form.forms import BaseModelForm

from ..models import TimePointStatus


class TimePointStatusForm(BaseModelForm):

    def clean(self):
        cleaned_data = super(TimePointStatusForm, self).clean()
        if cleaned_data.get('status') == 'feedback' and not cleaned_data.get('comment'):
            raise ValidationError('If feedback is being given, please provide a fully detailed description in the comment box below')

        if cleaned_data.get('subject_withdrew') == 'Yes' and cleaned_data.get('reasons_withdrawn') == 'N/A':
            raise ValidationError('If subject is withdrawing, REASON for withdrawal cannot be NOT APPLICABLE')

        if cleaned_data.get('subject_withdrew') == 'Yes' and not cleaned_data.get('withdraw_datetime'):
            raise ValidationError('If subject is withdrawing, please provide withdrawal date')

        self.instance.validate_status(exception_cls=ValidationError)
        return cleaned_data

    class Meta:
        model = TimePointStatus
