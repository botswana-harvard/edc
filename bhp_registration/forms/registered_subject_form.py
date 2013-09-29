from ...bhp_base_form.forms import BaseModelForm
from ..models import RegisteredSubject


class RegisteredSubjectForm (BaseModelForm):
    """Form for the RegisteredSubject model."""

    class Meta:
        model = RegisteredSubject
