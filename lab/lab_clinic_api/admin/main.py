from django.contrib import admin
from edc.export.actions import export_as_csv_action
from edc.base.admin.admin import BaseModelAdmin
from ..forms import ResultForm, ResultItemForm
from ..models import (Receive, Aliquot, Result, ResultItem, Review, Order, Panel, TestCode,
                     AliquotType, TestCodeGroup, AliquotCondition)
from ..actions import recalculate_grading, flag_as_reviewed, unflag_as_reviewed, refresh_order_status


class TestCodeAdmin(BaseModelAdmin):
    list_display = ('code', 'name', 'edc_code', 'edc_name')
    list_filter = ('test_code_group', )
    search_fields = ('code', 'name', 'edc_code', 'edc_name', 'test_code_group__code', 'test_code_group__name')
admin.site.register(TestCode, TestCodeAdmin)


class TestCodeGroupAdmin(BaseModelAdmin):
    list_display = ('code', 'name')
admin.site.register(TestCodeGroup, TestCodeGroupAdmin)


class ReviewAdmin(BaseModelAdmin):
    list_display = ('title', 'review_status', 'created', 'modified', 'user_created', 'user_modified')
    fields = ('title', 'review_status', 'comment')
    search_fields = ('title', 'comment')
    list_filter = ('review_status', 'created', 'modified', 'user_created', 'user_modified')
    readonly_fields = ('title', 'review_status')
admin.site.register(Review, ReviewAdmin)


