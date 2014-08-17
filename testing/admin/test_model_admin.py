from django.contrib import admin

from apps.admin_supplemental_fields.classes import SupplementalFields
from edc.base.modeladmin.admin import BaseModelAdmin

from ..forms import TestModelForm
from ..models import TestModel, TestM2m, TestForeignKey


class TestModelAdmin(BaseModelAdmin):

    form = TestModelForm
    fields = ('f1', 'f2', 'f3', 'f4', 'f5')
    supplimental_fields = SupplementalFields(('f3', 'f4'), p=0.1)

admin.site.register(TestModel, TestModelAdmin)


class TestM2mAdmin(BaseModelAdmin):

    pass

admin.site.register(TestM2m, TestM2mAdmin)


class TestForeignKeyAdmin(BaseModelAdmin):

    pass

admin.site.register(TestForeignKey, TestForeignKeyAdmin)
