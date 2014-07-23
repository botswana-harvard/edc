from subject.off_study.models import BaseOffStudy


class TestOffStudy(BaseOffStudy):

    def get_requires_consent(self):
        return False

    def get_visit_model_app(self):
        return 'visit_tracking'

    class Meta:
        app_label = 'testing'
