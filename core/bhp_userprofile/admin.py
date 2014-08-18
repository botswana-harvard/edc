from django.contrib import admin
from edc.base.modeladmin.admin import BaseModelAdmin
from .models import UserProfile


class UserProfileAdmin(BaseModelAdmin):
    list_display = ('user', 'initials')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
admin.site.register(UserProfile, UserProfileAdmin)
