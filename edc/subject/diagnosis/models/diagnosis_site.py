from edc_base.model.models import BaseListModel


class DiagnosisSite (BaseListModel):

    class Meta:
        app_label = 'diagnosis'
        db_table = 'bhp_diagnosis_site'
