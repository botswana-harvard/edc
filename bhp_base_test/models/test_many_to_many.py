from edc_lib.base_model.models.base_list_model import BaseListModel


class TestManyToMany(BaseListModel):

    class Meta:
        app_label = 'bhp_base_model'
