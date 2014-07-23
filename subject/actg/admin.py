from django.contrib import admin
from base.modeladmin.admin import BaseModelAdmin
from .models import Appendix40


class Appendix40Admin(BaseModelAdmin):

    list_display = ('code', 'short_description')

    search_fields = ('code', 'short_description', 'full_description')

    readonly_fields = ('code', 'short_description', 'full_description')

admin.site.register(Appendix40, Appendix40Admin)
