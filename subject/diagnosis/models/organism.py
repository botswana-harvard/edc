from edc.base.model.models import BaseListModel


class Organism (BaseListModel):

    class Meta:
        app_label = 'diagnosis'
        db_table = 'bhp_diagnosis_organism'
