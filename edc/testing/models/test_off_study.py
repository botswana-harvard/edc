from edc.subject.off_study.models import BaseOffStudy
from edc.entry_meta_data.managers import EntryMetaDataManager
from edc.testing.models.test_visit import TestVisit


class TestOffStudy(BaseOffStudy):

    entry_meta_data_manager = EntryMetaDataManager(TestVisit)

    def get_requires_consent(self):
        return False

    def get_visit_model_app(self):
        return 'visit_tracking'

    class Meta:
        app_label = 'testing'
