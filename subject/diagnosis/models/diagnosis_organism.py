from base.model.models import BaseListModel


class DiagnosisOrganism (BaseListModel):

    class Meta:
        app_label = 'diagnosis'
        db_table = 'bhp_diagnosis_organism'
