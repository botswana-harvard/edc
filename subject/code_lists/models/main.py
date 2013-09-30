from django.db import models
from .base_code_list import BaseCodeList


class WcsDxAdult(BaseCodeList):

    """WhoClinicalStagingDxAdult"""

    list_ref = models.CharField("List Reference",
        max_length=100,
        blank=True,
        )

    class Meta:
        app_label = "code_lists"
        db_table = "bhp_code_lists_wcsdxadult"  # TODO: remove when db schema is changed


class WcsDxPed(BaseCodeList):

    """WhoClinicalStagingDxPediatric"""

    list_ref = models.CharField("List Reference",
        max_length=100,
        blank=True,
        )

    class Meta:
        app_label = "code_lists"
        db_table = "bhp_code_lists_wcsdxped"  # TODO: remove when db schema is changed


class MedicationCode (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "code_lists"
        db_table = "bhp_code_lists_medicationcode"  # TODO: remove when db schema is changed


class BodySiteCode (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "code_lists"
        db_table = "bhp_code_lists_bodysitecode"  # TODO: remove when db schema is changed


class OrganismCode (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "code_lists"
        db_table = "bhp_code_lists_organismcode"  # TODO: remove when db schema is changed


class ArvCode (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "code_lists"
        db_table = "bhp_code_lists_arvcode"  # TODO: remove when db schema is changed


class ArvDoseStatus (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "code_lists"
        db_table = "bhp_code_lists_arvdosestatus"  # TODO: remove when db schema is changed


class ArvModificationCode (BaseCodeList):
    list_ref = models.CharField("List Reference",
        max_length=35)

    class Meta:
        app_label = "code_lists"
        db_table = "bhp_code_lists_arvmodificationcode"  # TODO: remove when db schema is changed
