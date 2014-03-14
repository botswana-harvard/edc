from collections import namedtuple

from django.core.exceptions import ImproperlyConfigured

from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.models import StudySpecific, StudySite
from edc.device.device.classes import Device
from edc.lab.lab_clinic_api.models import AliquotType, ProcessingProfile, ProcessingProfileItem
from edc.subject.appointment.models import Configuration
from edc.subject.consent.models import ConsentCatalogue

AliquotTypeTuple = namedtuple('AliquotTypeTuple', 'name alpha_code numeric_code')
ProfileTuple = namedtuple('ProfileItemTuple', 'profile_name alpha_code')
ProfileItemTuple = namedtuple('ProfileItemTuple', 'profile_name alpha_code volume count')


class BaseAppConfiguration(object):

    appointment_configuration = None
    consent_catalogue_list = None
    consent_catalogue_setup = None
    lab_clinic_api_setup = None
    study_site_setup = None
    study_variables_setup = None

    def __init__(self):
        ContentTypeMap.objects.populate()
        ContentTypeMap.objects.sync()
        self.update_or_create_appointment_setup()
        self.update_or_create_study_variables()
        self.update_or_create_consent_catalogue()
        self.update_or_create_study_site()
        self.update_or_create_lab_clinic_api()

    def update_or_create_lab_clinic_api(self):
        for item in self.lab_clinic_api_setup.get('aliquot_type'):
            if AliquotType.objects.filter(name=item.name):
                aliquot_type = AliquotType.objects.get(name=item.name)
                aliquot_type.alpha_code = item.alpha_code
                aliquot_type.numeric_code = item.numeric_code
                aliquot_type.save()
            else:
                AliquotType.objects.create(name=item.name, alpha_code=item.alpha_code, numeric_code=item.numeric_code)
        # create profiles
        for item in self.lab_clinic_api_setup.get('processing_profile'):
            aliquot_type = AliquotType.objects.get(alpha_code=item.alpha_code)
            if not ProcessingProfile.objects.filter(profile_name=item.profile_name):
                ProcessingProfile.objects.create(profile_name=item.profile_name, aliquot_type=aliquot_type)
            else:
                processing_profile = ProcessingProfile.objects.get(profile_name=item.profile_name)
                processing_profile.aliquot_type = aliquot_type
                processing_profile.save()
        # add profile items
        for item in self.lab_clinic_api_setup.get('processing_profile_item'):
            processing_profile = ProcessingProfile.objects.get(profile_name=item.profile_name)
            aliquot_type = AliquotType.objects.get(alpha_code=item.alpha_code)
            if not ProcessingProfileItem.objects.filter(processing_profile=processing_profile, aliquot_type=aliquot_type):
                ProcessingProfileItem.objects.create(processing_profile=processing_profile, aliquot_type=aliquot_type, volume=item.volume, count=item.count)
            else:
                profile_item = ProcessingProfileItem.objects.get(processing_profile=processing_profile, aliquot_type=aliquot_type)
                profile_item.volume = item.volume
                profile_item.count = item.count
                profile_item.save()

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
        for catalogue_setup in self.consent_catalogue_list:
            catalogue_setup.update({'content_type_map': ContentTypeMap.objects.get(model=catalogue_setup.get('content_type_map').lower())})
            if not ConsentCatalogue.objects.filter(**catalogue_setup).exists():
                ConsentCatalogue.objects.create(**catalogue_setup)
            else:
                ConsentCatalogue.objects.filter(**catalogue_setup).update(**catalogue_setup)

    def update_or_create_study_site(self):
        if self.study_site_setup and not StudySite.objects.filter(**self.study_site_setup).exists():
            StudySite.objects.create(**self.study_site_setup)
        if not Device().is_server() and StudySite.objects.all().count() > 1:
            raise ImproperlyConfigured('There has to be only one Study Site record on bhp_variables. Got {0}'.format(StudySite.objects.all().count()))
