from edc.core.bhp_variables.models import StudySite


def default_study_site(attribute, value):
    try:
        site = StudySite.objects.get(**{attribute: value})
    except StudySite.DoesNotExist:
        return None
    return site
