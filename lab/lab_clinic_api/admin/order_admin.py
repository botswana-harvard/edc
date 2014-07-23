from django.contrib import admin

from base.modeladmin.admin import BaseModelAdmin

from ..models import Order

from ..actions import refresh_order_status


class OrderAdmin(BaseModelAdmin):
    date_hierarchy = 'order_datetime'
    list_display = ("order_identifier", "receive_identifier", "req", "to_receive", "to_result", "subject_identifier", "panel", "order_datetime", 'status', 'created', 'modified', 'import_datetime')
    search_fields = ('aliquot__receive__registered_subject__subject_identifier', "order_identifier", "aliquot__receive__receive_identifier")
    list_filter = ('status', 'import_datetime', 'aliquot__aliquot_condition', 'panel__edc_name')
    list_per_page = 15
    actions = [refresh_order_status, ]

    def get_readonly_fields(self, request, obj):
        return ['aliquot', 'status', 'order_datetime', 'comment']
admin.site.register(Order, OrderAdmin)
