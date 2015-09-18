from edc_base.model.models import BaseListModel


class DiagnosisCode (BaseListModel):
    pass

    class Meta:
        app_label = 'diagnosis'
        db_table = 'bhp_diagnosis_code'
        verbose_name = "Code"
