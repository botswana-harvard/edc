from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin

from ..models import Processing


class ProcessingAdmin(BaseModelAdmin):

    list_display = ('aliquot', 'processing_profile', 'created', 'modified', 'user_created', 'user_modified')

    search_fields = ('aliquot__aliquot_identifier', 'processing_profile__profile_name', 'aliquot__aliquot_type__name', 'aliquot__aliquot_type__alpha_code', 'aliquot__aliquot_type__numeric_code')

    list_filter = ('processing_profile', 'created', 'modified', 'user_created', 'user_modified')

admin.site.register(Processing, ProcessingAdmin)
