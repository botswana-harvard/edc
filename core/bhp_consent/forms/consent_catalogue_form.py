from edc.core.bhp_base_form.forms import BaseModelForm


class ConsentCatalogueForm (BaseModelForm):

    def clean(self, consent_instance=None):
        cleaned_data = self.cleaned_data
        return cleaned_data
