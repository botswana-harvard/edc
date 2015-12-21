from django import forms
from edc.base.form.forms import BaseModelForm
from edc.subject.appointment.models import Appointment
from edc.subject.appointment_helper.models import AppointmentMixin


class MembershipFormForm(BaseModelForm):

    class Meta:
        model = Appointment

    def clean(self):
        cleaned_data = self.cleaned_data
        if not issubclass(cleaned_data.get('content_type_map').model_class(), AppointmentMixin):
            raise forms.ValidationError('Membership forms must be a subclass of AppointmentMixin. See module bhp_appointment_helper.')
        return cleaned_data
