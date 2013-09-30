from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from ..models import Producer
from ..actions import reset_producer_status


class ProducerAdmin(BaseModelAdmin):

    list_display = ('name', 'url', 'is_active', 'sync_datetime', 'sync_status', 'comment')
    list_filter = ('is_active', 'sync_datetime', 'sync_status',)

    actions = [reset_producer_status]

admin.site.register(Producer, ProducerAdmin)
