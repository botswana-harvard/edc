from django.db import models

from .base_code_list import BaseCodeList


class SsxCode (BaseCodeList):
    list_ref = models.CharField(
        verbose_name="List Reference",
        max_length=35)

    class Meta:
        app_label = "code_lists"
