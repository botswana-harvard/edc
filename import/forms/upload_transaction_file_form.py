from django import forms


class UploadTransactionFileForm(forms.ModelForm):

    def clean(self):

        cleaned_data = super(UploadTransactionFileForm, self).clean()

        self.instance.check_for_transactions(cleaned_data.get('transaction_file'), forms.ValidationError)

        return cleaned_data
