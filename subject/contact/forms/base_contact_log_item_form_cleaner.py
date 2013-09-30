from django import forms


class BaseContactLogItemFormCleaner (object):

    def clean(self, cleaned_data):
        if not cleaned_data.get('is_contacted', None):
            raise forms.ValidationError('Please select Yes or No')
        if cleaned_data.get('is_contacted').lower() == 'no' and cleaned_data.get('information_provider'):
            raise forms.ValidationError('You wrote contact was NOT made yet have recorded the information provider. Please correct.')
        if cleaned_data.get('is_contacted').lower() == 'yes' and not cleaned_data.get('information_provider'):
            raise forms.ValidationError('You wrote contact was made. Please indicate the information provider. Please correct.')
        return cleaned_data
