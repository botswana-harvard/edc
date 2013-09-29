from django import forms
from edc_core.bhp_base_form.forms import BaseModelForm


class BaseConsentUpdateForm (BaseModelForm):
    def clean(self, consent_instance_field_name, consent_instance=None):
        cleaned_data = self.cleaned_data
        consent_version = cleaned_data.get('consent_version', None)
        if not consent_version and consent_instance:
            # get the consent version and check if duplicate
            #consent_version = ConsentHelper(self._meta.model(consent_instance), forms.ValidationError).get_current_consent_version()
            options = {consent_instance_field_name: consent_instance, 'consent_version': consent_version}
            #if consent_version == 1:
            #    raise forms.ValidationError('Consent update cannot have a consent datetime within the consent period for version 1.')
            if self._meta.model.objects.filter(**options).exists() and not cleaned_data.get('id', None):
                raise forms.ValidationError('Consent update for consent version {0} already exists.'.format(consent_version))

        return cleaned_data
