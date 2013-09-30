from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from edc.core.admin_supplemental_fields.classes import SupplementalFields, ConditionalFields
from ..models import TestModel, TestM2m, TestForeignKey
from ..forms import TestModelForm


class TestModelAdmin(BaseModelAdmin):

    form = TestModelForm
    fields = ('f1', 'f2', 'f3', 'f4', 'f5')
    supplimental_fields = SupplementalFields(('f3', 'f4'), p=0.1)

    conditional_fields = ConditionalFields(('f3', ), gender='M', age=(18, 64), bcpp_subject__monthsrecentpartner__first_haart='Yes')

admin.site.register(TestModel, TestModelAdmin)


class TestM2mAdmin(BaseModelAdmin):

    pass

admin.site.register(TestM2m, TestM2mAdmin)


class TestForeignKeyAdmin(BaseModelAdmin):

    pass

admin.site.register(TestForeignKey, TestForeignKeyAdmin)
