from django.contrib import admin

from ..models import NotificationPlan


class NotificationPlanAdmin (admin.ModelAdmin):

    list_display = ('name', 'created', 'modified')

admin.site.register(NotificationPlan, NotificationPlanAdmin)
