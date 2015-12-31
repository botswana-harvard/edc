from edc.entry_meta_data.models import MetaDataMixin
from edc_visit_tracking.models import VisitTrackingModelMixin, PreviousVisitMixin


class TestVisit(MetaDataMixin, PreviousVisitMixin, VisitTrackingModelMixin):

    REQUIRES_PREVIOUS_VISIT = True

    def custom_post_update_entry_meta_data(self):
        pass

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'testing'


class TestVisit2(MetaDataMixin, PreviousVisitMixin, VisitTrackingModelMixin):

    REQUIRES_PREVIOUS_VISIT = True

    def custom_post_update_entry_meta_data(self):
        pass

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'testing'


class TestSubjectVisit(VisitTrackingModelMixin):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'testing'


class TestSubjectVisitTwo(VisitTrackingModelMixin):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'testing'


class TestSubjectVisitThree(VisitTrackingModelMixin):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'testing'
