from django.contrib import admin
from edc.core.bhp_base_admin.admin import BaseModelAdmin
from ..models import RequestLog


class RequestLogAdmin(BaseModelAdmin):

    list_display = ('producer', 'request_datetime', 'status', 'comment')

admin.site.register(RequestLog, RequestLogAdmin)
