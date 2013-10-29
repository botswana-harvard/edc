from django.contrib import admin
from django.db import models
from django.test import TestCase
from edc.base.model.models import BaseUuidModel
from ..admin import SupplementalModelAdmin


class TestSuppModel(BaseUuidModel):

    field1 = models.CharField(max_length=10, null=True)
    field2 = models.CharField(max_length=10, null=True)
    field3 = models.CharField(max_length=10, null=True, blank=False)
    field4 = models.CharField(max_length=10, null=True, blank=False)
    field5 = models.CharField(max_length=10, null=True)


class TestSuppModelAdmin(SupplementalModelAdmin):
    pass
admin.site.register(TestSuppModel, TestSuppModelAdmin)


class TestSupplementalFields(TestCase):

    def test_save_model(self):
        test_model = TestSuppModel()
        model_admin = TestSuppModelAdmin()