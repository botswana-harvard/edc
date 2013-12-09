from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin, BaseStackedInline
from ..models import DispatchContainerRegister, DispatchItemRegister
from ..actions import return_dispatched_containers


class DispatchItemRegisterInline(BaseStackedInline):
    model = DispatchItemRegister
    extra = 0


class DispatchContainerRegisterAdmin(BaseModelAdmin):
    date_hierarchy = 'dispatch_datetime'
    ordering = ['-created', ]
    list_display = (
        'producer',
        'to_items',
        'container_model_name',
        'container_identifier',
        'created',
        'is_dispatched',
        'dispatch_datetime',
        'return_datetime'
        )
    list_filter = (
        'producer',
        'container_identifier',
        'created',
        'is_dispatched',
        'dispatch_datetime',
        'return_datetime'
        )
    search_fields = ('id', 'container_identifier', )
    inlines = [DispatchItemRegisterInline, ]
    actions = [return_dispatched_containers, ]
admin.site.register(DispatchContainerRegister, DispatchContainerRegisterAdmin)
