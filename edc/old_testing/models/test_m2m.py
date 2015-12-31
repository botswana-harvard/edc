from edc_base.model.models import BaseListModel


class TestM2m(BaseListModel):

    class Meta:
        app_label = 'testing'
