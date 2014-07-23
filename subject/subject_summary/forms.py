from base.form.forms import BaseModelForm
from .models import Link


class LinkForm (BaseModelForm):

    class Meta:
        model = Link
