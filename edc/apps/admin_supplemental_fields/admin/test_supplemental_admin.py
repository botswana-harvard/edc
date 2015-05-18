from django.contrib import admin

from edc.base.modeladmin.admin import BaseModelAdmin

from ..admin import SupplementalModelAdminMixin
from ..classes import SupplementalFields
from ..forms import TestSupplementalForm
from ..models import TestSupplemental


class TestSupplementalAdmin(SupplementalModelAdminMixin, BaseModelAdmin):

    form = TestSupplementalForm

    supplemental_fields = SupplementalFields(('f2', 'f3'), p=0.09, group='TEST', grouping_field='f1')

    fields = ('f1', 'f2', 'f3', 'f4', 'f5')

admin.site.register(TestSupplemental, TestSupplementalAdmin)
