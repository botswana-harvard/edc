from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from ..models import TestScheduledModel, TestSubjectLocator, EncryptedTestModel


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
