from edc.base.model.models import BaseListModel


class DeathCauseInfo (BaseListModel):
    class Meta:
        ordering = ['display_index']
        app_label = 'adverse_event'
        db_table = 'bhp_adverse_deathcauseinfo'  # TODO: remove after changing DB Schema


class DeathCauseCategory (BaseListModel):
    class Meta:
        ordering = ['display_index']
        app_label = 'adverse_event'
        db_table = 'bhp_adverse_deathcausecategory'  # TODO: remove after changing DB Schema


class DeathMedicalResponsibility (BaseListModel):
    class Meta:
        ordering = ['display_index']
        app_label = 'adverse_event'
        db_table = 'bhp_adverse_deathmedicalresponsibility'  # TODO: remove after changing DB Schema


class DeathReasonHospitalized (BaseListModel):
    class Meta:
        ordering = ['display_index']
        app_label = 'adverse_event'
        db_table = 'bhp_adverse_deathreasonhospitalized'  # TODO: remove after changing DB Schema
