from datetime import datetime
from django.contrib import messages


def flag_as_verified_against_paper(modeladmin, request, queryset, **kwargs):
    """ Flags instance as verified against the paper document."""

    for qs in queryset:
        qs.is_verified = True
        qs.is_verified_datetime = datetime.today()
        qs.save(consent_verification=True)
        messages.add_message(request, messages.SUCCESS, 'Consent for {0} has been verified.'.format(qs.subject_identifier))
flag_as_verified_against_paper.short_description = "Verified against paper document"


def unflag_as_verified_against_paper(modeladmin, request, queryset, **kwargs):
    """ UnFlags instance as verified."""

    for qs in queryset:
        qs.is_verified = False
        qs.is_verified_datetime = datetime.today()
        qs.save(consent_verification=True)

unflag_as_verified_against_paper.short_description = "Un-verify"
