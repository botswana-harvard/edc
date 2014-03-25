from edc.base.form.forms import BaseModelForm
from ..models import AdditionalAppointmentLabEntry


class AdditionalAppointmentLabEntryForm (BaseModelForm):

    class Meta:
        model = AdditionalAppointmentLabEntry
