from django.contrib import admin
from edc.base.modeladmin.admin import BaseModelAdmin
from ..models import ModelHelpText
from ..forms import  ModelHelpTextForm


class ModelHelpTextAdmin(BaseModelAdmin):
    form = ModelHelpTextForm
    list_display = ('app_label', 'module_name', 'field_name', 'url', 'status')
    list_filter = ('app_label', 'module_name',)
admin.site.register(ModelHelpText, ModelHelpTextAdmin)
