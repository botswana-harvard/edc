from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin

from ..actions import flag_as_reviewed, unflag_as_reviewed
from ..forms import ResultForm
from ..models import Result


class ResultAdmin(BaseModelAdmin):
    date_hierarchy = 'result_datetime'
    actions = [flag_as_reviewed, unflag_as_reviewed]
    form = ResultForm
    search_fields = ("result_identifier", "subject_identifier",
                     "receive_identifier",
                     "order__order_identifier",
                     'order__panel__name')
    list_display = (
        "result_identifier",
        'report',
        'reviewed',
        "subject_identifier",
        'panel',
        "result_datetime",
        'to_order',
        'to_items',
        "release_status",
        "release_datetime",
        'import_datetime')
    radio_fields = {"release_status": admin.VERTICAL}
    list_filter = ("release_status", 'reviewed', "result_datetime", 'import_datetime')
    list_per_page = 15

    def get_readonly_fields(self, request, obj):
        return [field.name for field in obj._meta.fields if field.editable]

admin.site.register(Result, ResultAdmin)
