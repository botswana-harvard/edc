from django.contrib import admin
from base.modeladmin.admin import BaseModelAdmin
from ..models import TestScheduledModel, TestScheduledModel1, TestScheduledModel2, TestScheduledModel3, TestSubjectLocator, EncryptedTestModel


class TestScheduledModelAdmin(BaseModelAdmin):
    pass
admin.site.register(TestScheduledModel, TestScheduledModelAdmin)


class TestScheduledModel1Admin(BaseModelAdmin):
    pass
admin.site.register(TestScheduledModel1, TestScheduledModel1Admin)


class TestScheduledModel2Admin(BaseModelAdmin):
    pass
admin.site.register(TestScheduledModel2, TestScheduledModel2Admin)


class TestScheduledModel3Admin(BaseModelAdmin):
    pass
admin.site.register(TestScheduledModel3, TestScheduledModel3Admin)


class TestSubjectLocatorAdmin(BaseModelAdmin):
    pass
admin.site.register(TestSubjectLocator, TestSubjectLocatorAdmin)


class EncryptedTestModelAdmin (admin.ModelAdmin):

    list_display = ('firstname', 'lastname')
    search_fields = ('firstname', 'lastname')

admin.site.register(EncryptedTestModel, EncryptedTestModelAdmin)
