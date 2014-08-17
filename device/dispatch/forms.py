from django import forms
from edc.device.sync.models import Producer


class DispatchForm(forms.Form):
    producer = forms.ModelChoiceField(
        queryset=Producer.objects.all().order_by('name'),
        required=False)
