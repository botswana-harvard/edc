from django.contrib import admin
from .models import UserProfile


class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'initials')
    search_fields = ['user__username', 'user__first_name', 'user__last_name']
admin.site.register(UserProfile, UserProfileAdmin)
