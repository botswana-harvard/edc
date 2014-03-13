from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin, BaseTabularInline

from ..models import ProcessingProfile, ProcessingProfileItem


class ProcessingProfileItemAdmin(BaseModelAdmin):

    list_display = ('processing_profile', 'aliquot_type', 'created', 'modified', 'user_created', 'user_modified')

    search_fields = ('processing_profile__profile_name', 'aliquot_type__name', 'aliquot_type__alpha_code', 'aliquot_type__numeric_code')

    list_filter = ('aliquot_type__name', 'aliquot_type__alpha_code', 'aliquot_type__numeric_code', 'created', 'modified', 'user_created', 'user_modified')

admin.site.register(ProcessingProfileItem, ProcessingProfileItemAdmin)


class ProcessingProfileItemInlineAdmin(BaseTabularInline):
    model = ProcessingProfileItem


class ProcessingProfileAdmin(BaseModelAdmin):

    list_display = ('profile_name', 'aliquot_type', 'created', 'modified', 'user_created', 'user_modified')

    search_fields = ('profile_name', 'aliquot_type__name', 'aliquot_type__alpha_code', 'aliquot_type__numeric_code')

    list_filter = ('aliquot_type__name', 'aliquot_type__alpha_code', 'aliquot_type__numeric_code', 'created', 'modified', 'user_created', 'user_modified')

    inlines = [ProcessingProfileItemInlineAdmin]

admin.site.register(ProcessingProfile, ProcessingProfileAdmin)
