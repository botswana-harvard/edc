from django.contrib import admin

from ..models import Notification


class NotificationAdmin (admin.ModelAdmin):

    date_hierarchy = 'notification_datetime'
    list_display = ('notification_plan_name', 'notification_datetime', 'status', 'sent', 'sent_datetime', 'subject', 'modified')
    list_filter = ('notification_datetime', 'status', 'sent', 'sent_datetime', 'modified')
admin.site.register(Notification, NotificationAdmin)
