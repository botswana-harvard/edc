from edc.base.model.models import BaseListModel


class Site (BaseListModel):

    class Meta:
        app_label = 'diagnosis'
        db_table = 'bhp_diagnosis_site'
