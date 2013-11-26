from django import forms

from ..models import BaseReport


class ReportForm(forms.Form):
    reports = forms.ModelChoiceField(queryset=BaseReport.objects.all().order_by('report_name'))
