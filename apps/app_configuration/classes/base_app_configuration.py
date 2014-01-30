from django.core.exceptions import ImproperlyConfigured
from edc.subject.appointment.models import Configuration
from edc.core.bhp_variables.models import StudySpecific, StudySite
from edc.subject.consent.models import ConsentCatalogue


class BaseAppConfiguration(object):

    appointment_configuration = None
    study_variables_setup = None
    consent_catalogue_setup = None
    study_site_setup = None

    def __init__(self):
        self.update_or_create_appointment_setup()
        self.update_or_create_study_variables()
        self.update_or_create_consent_catalogue()
        self.update_or_create_study_site()

    def update_or_create_appointment_setup(self):

        if Configuration.objects.all().count() == 0:
            Configuration.objects.create(**self.appointment_configuration)
        else:
            Configuration.objects.all().update(**self.appointment_configuration)

    def update_or_create_study_variables(self):

        if StudySpecific.objects.all().count() == 0:
            StudySpecific.objects.create(**self.study_variables_setup)
        else:
            StudySpecific.objects.all().update(**self.study_variables_setup)

    def update_or_create_consent_catalogue(self):

        if ConsentCatalogue.objects.all().count() == 0:
            ConsentCatalogue.objects.create(**self.consent_catalogue_setup)
        else:
            ConsentCatalogue.objects.all().update(**self.consent_catalogue_setup)

    def update_or_create_study_site(self):
        if not StudySite.objects.filter(site_code=self.study_site_setup['site_mapper'].map_code).exists():
            StudySite.objects.create(site_name=self.study_site_setup['site_mapper'].map_area,
                                         site_code=self.study_site_setup['site_mapper'].map_code)
        if StudySite.objects.all().count() > 1:
            raise ImproperlyConfigured('There has to be only one Study Site record on bhp_variables. Got {0}'.format(StudySite.objects.all().count()))


