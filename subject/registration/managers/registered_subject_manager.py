from edc.subject.subject.managers import BaseSubjectManager


class RegisteredSubjectManager(BaseSubjectManager):

    def get_by_natural_key(self, subject_identifier_as_pk):
        return self.get(registered_subject__subject_identifier_as_pk=subject_identifier_as_pk)
