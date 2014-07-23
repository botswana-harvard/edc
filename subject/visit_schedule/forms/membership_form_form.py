from django import forms
from base.form.forms import BaseModelForm
from subject.appointment.models import Appointment
from subject.appointment_helper.models import  BaseAppointmentMixin


class MembershipFormForm(BaseModelForm):

    class Meta:
        model = Appointment

    def clean(self):
        cleaned_data = self.cleaned_data
        if not issubclass(cleaned_data.get('content_type_map').model_class(), BaseAppointmentMixin):
            raise forms.ValidationError('Membership forms must be a subclass of BaseAppointmentMixin. See module bhp_appointment_helper.')
        return cleaned_data
