from django.contrib import admin
from edc_core.bhp_crypto.admin import BaseCryptorModelAdmin
from ..models import SubjectIdentifierAuditTrail


class SubjectIdentifierAuditTrailAdmin(BaseCryptorModelAdmin):

    list_display = (
        'subject_identifier',
        'date_allocated',
        )
    list_per_page = 15

admin.site.register(SubjectIdentifierAuditTrail, SubjectIdentifierAuditTrailAdmin)
