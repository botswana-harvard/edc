from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from ..actions import flag_as_verified_against_paper, unflag_as_verified_against_paper


class BaseConsentModelAdmin(BaseModelAdmin):
    """Serves as the ModelAdmin for all consent models."""
    def __init__(self, *args, **kwargs):

        super(BaseConsentModelAdmin, self).__init__(*args, **kwargs)
        self.search_fields = ['id', 'subject_identifier', 'first_name', 'last_name', 'identity', ]
        self.list_display = ['subject_identifier', 'is_verified', 'first_name', 'initials', 'gender', 'dob',
                             'consent_datetime', 'created', 'modified', 'user_created', 'user_modified', ]
        self.actions.append(flag_as_verified_against_paper)
        self.actions.append(unflag_as_verified_against_paper)
        self.list_filter = [
            'gender',
            'is_verified',
            'language',
            'may_store_samples',
            'study_site',
            'is_literate',
            'consent_datetime',
            'created',
            'modified',
            'user_created',
            'user_modified',
            'hostname_created']
        self.fields = [
            'subject_identifier',
            'first_name',
            'last_name',
            'initials',
            'language',
            'is_literate',
            'witness_name',
            'consent_datetime',
            'study_site',
            'gender',
            'dob',
            'guardian_name',
            'is_dob_estimated',
            'identity',
            'identity_type',
            'confirm_identity',
            'is_incarcerated',
            'may_store_samples',
            'comment',
            'consent_reviewed',
            'study_questions',
            'assessment_score',
            'consent_copy']

        self.radio_fields = {
            "language": admin.VERTICAL,
            "gender": admin.VERTICAL,
            "study_site": admin.VERTICAL,
            "is_dob_estimated": admin.VERTICAL,
            "identity_type": admin.VERTICAL,
            "may_store_samples": admin.VERTICAL,
            "consent_reviewed": admin.VERTICAL,
            "study_questions": admin.VERTICAL,
            "assessment_score": admin.VERTICAL,
            "consent_copy": admin.VERTICAL,
            "is_literate": admin.VERTICAL}

    #override to disallow subject to be changed
    def get_readonly_fields(self, request, obj=None):
        super(BaseConsentModelAdmin, self).get_readonly_fields(request, obj)
        if obj:  # In edit mode
            return (
                'subject_identifier',
                'subject_identifier_as_pk',
                'study_site',
                'consent_datetime',) + self.readonly_fields
        else:
            return ('subject_identifier', 'subject_identifier_as_pk',) + self.readonly_fields
