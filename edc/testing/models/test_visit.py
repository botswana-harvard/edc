from edc.subject.visit_tracking.models import BaseVisitTracking
from edc.entry_meta_data.models import MetaDataMixin
from edc.subject.visit_tracking.models import PreviousVisitMixin


class TestVisit(MetaDataMixin, PreviousVisitMixin, BaseVisitTracking):

    REQUIRES_PREVIOUS_VISIT = True

    def custom_post_update_entry_meta_data(self):
        pass

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'testing'


class TestVisit2(MetaDataMixin, PreviousVisitMixin, BaseVisitTracking):

    REQUIRES_PREVIOUS_VISIT = True

    def custom_post_update_entry_meta_data(self):
        pass

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'testing'


class TestSubjectVisit(BaseVisitTracking):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'testing'


class TestSubjectVisitTwo(BaseVisitTracking):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'testing'


class TestSubjectVisitThree(BaseVisitTracking):

    def get_requires_consent(self):
        return False

    class Meta:
        app_label = 'testing'
