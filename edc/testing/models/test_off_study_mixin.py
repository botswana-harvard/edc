from edc.subject.off_study.mixins import OffStudyMixin

from .test_base_off_study import TestBaseOffStudy


class TestOffStudyMixin(OffStudyMixin):

    OFF_STUDY_MODEL =  TestBaseOffStudy
