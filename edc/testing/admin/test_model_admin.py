from django.contrib import admin

from edc_base.modeladmin.admin import BaseModelAdmin

from ..forms import TestModelForm
from ..models import TestModel, TestM2m, TestForeignKey


class TestModelAdmin(BaseModelAdmin):

    form = TestModelForm
    fields = ('f1', 'f2', 'f3', 'f4', 'f5')

admin.site.register(TestModel, TestModelAdmin)


class TestM2mAdmin(BaseModelAdmin):

    pass

admin.site.register(TestM2m, TestM2mAdmin)


class TestForeignKeyAdmin(BaseModelAdmin):

    pass

admin.site.register(TestForeignKey, TestForeignKeyAdmin)
