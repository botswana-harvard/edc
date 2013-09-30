from django.contrib import admin
from edc.core.bhp_base_admin.admin import BaseModelAdmin
from ..models import ConsentCatalogue
from ..forms import ConsentCatalogueForm


class ConsentCatalogueAdmin(BaseModelAdmin):
    form = ConsentCatalogueForm
    list_display = ('name', 'version', 'consent_type', 'start_datetime', 'end_datetime')
    list_filter = ('consent_type', 'created')
admin.site.register(ConsentCatalogue, ConsentCatalogueAdmin)
