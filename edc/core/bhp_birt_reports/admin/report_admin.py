from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..actions import process_report
from ..models import BaseReport
from ..models import ReportParameter


class ReportParameterAdmin(BaseModelAdmin):

    list_per_page = 15
    list_display = ('parameter_name', 'parameter_type',)
    list_filter = ('parameter_name', 'parameter_type',)
    search_fields = ('parameter_name', 'parameter_type',)
admin.site.register(ReportParameter, ReportParameterAdmin)


class ReportParameterInline(admin.TabularInline):

    model = ReportParameter
    extra = 1
    max_num = 5


class BaseReportAdmin(BaseModelAdmin):

    inlines = [ReportParameterInline, ]
    list_per_page = 15
    fields = ('report_name', 'report_url', 'is_active')
    search_fields = ('report_name', 'report_url', 'is_active')
    list_display = ('report_name', 'report_url', 'is_active')
    list_filter = ('report_name', 'is_active')
    actions = [process_report, ]
admin.site.register(BaseReport, BaseReportAdmin)
