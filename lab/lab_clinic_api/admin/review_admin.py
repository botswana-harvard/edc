from django.contrib import admin

from edc.base.admin.admin import BaseModelAdmin

from ..models import Review


class ReviewAdmin(BaseModelAdmin):
    list_display = ('title', 'review_status', 'created', 'modified', 'user_created', 'user_modified')
    fields = ('title', 'review_status', 'comment')
    search_fields = ('title', 'comment')
    list_filter = ('review_status', 'created', 'modified', 'user_created', 'user_modified')
    readonly_fields = ('title', 'review_status')
admin.site.register(Review, ReviewAdmin)
