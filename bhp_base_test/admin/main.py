from django.contrib import admin
from ...bhp_base_admin.admin import BaseModelAdmin
from ...bhp_base_test.models import TestScheduledModel, TestSubjectLocator
from ..models import EncryptedTestModel


class TestScheduledModelAdmin(BaseModelAdmin):
    pass
admin.site.register(TestScheduledModel, TestScheduledModelAdmin)


class TestSubjectLocatorAdmin(BaseModelAdmin):
    pass
admin.site.register(TestSubjectLocator, TestSubjectLocatorAdmin)


class EncryptedTestModelAdmin (admin.ModelAdmin):

    list_display = ('firstname', 'lastname')
    search_fields = ('firstname', 'lastname')

admin.site.register(EncryptedTestModel, EncryptedTestModelAdmin)
