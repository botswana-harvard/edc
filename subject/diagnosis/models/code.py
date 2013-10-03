from edc.base.model.models import BaseListModel


class Code (BaseListModel):
    pass

    class Meta:
        app_label = 'diagnosis'
        db_table = 'bhp_diagnosis_code'
        verbose_name = "Code"
