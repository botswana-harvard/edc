from edc.subject.visit_tracking.models import BaseVisitTracking


class TestVisit(BaseVisitTracking):

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
