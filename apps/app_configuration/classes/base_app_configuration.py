from django.core.exceptions import ImproperlyConfigured
from edc.subject.appointment.models import Configuration
from edc.core.bhp_variables.models import StudySpecific, StudySite
from edc.subject.consent.models import ConsentCatalogue
from edc.device.device.classes import Device


class BaseAppConfiguration(object):

    appointment_configuration = None
    study_variables_setup = None
    consent_catalogue_setup = None
    study_site_setup = None
    consent_catalogue_list = None

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
        for catalogue in self.consent_catalogue_list:
            if not ConsentCatalogue.objects.filter(**catalogue).exists():
                ConsentCatalogue.objects.create(**catalogue)
            #else:
            #    ConsentCatalogue.objects.update(**catalogue)

    def update_or_create_study_site(self):
        if self.study_site_setup and not StudySite.objects.filter(**self.study_site_setup).exists():
            StudySite.objects.create(**self.study_site_setup)
        if not Device().is_server() and StudySite.objects.all().count() > 1:
            raise ImproperlyConfigured('There has to be only one Study Site record on bhp_variables. Got {0}'.format(StudySite.objects.all().count()))


