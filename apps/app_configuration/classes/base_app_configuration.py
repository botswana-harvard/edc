from django.core.exceptions import ImproperlyConfigured

from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.models import StudySpecific, StudySite
from edc.device.device.classes import Device
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.appointment.models import Configuration
from edc.subject.consent.models import ConsentCatalogue
from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper

from lis.labeling.models import LabelPrinter


class BaseAppConfiguration(object):

    appointment_configuration = None
    consent_catalogue_list = None
    consent_catalogue_setup = None
    lab_clinic_api_setup = None
    lab_setup = None
    study_site_setup = None
    study_variables_setup = None

    def __init__(self):
        """Updates content type maps then runs each configuration method with the corresponding class attribute.

        Configuration methods update default data in supporting tables."""
        ContentTypeMapHelper().populate()
        ContentTypeMapHelper().sync()
        self.update_or_create_appointment_setup()
        self.update_or_create_study_variables()
        self.update_or_create_consent_catalogue()
        self.update_or_create_lab_clinic_api()
        self.update_or_create_lab()
        self.update_or_create_labeling()

    def update_or_create_lab_clinic_api(self):
        """Configure lab clinic api lsist tables.

        ..note:: see visit_schedule model where Panels are updated"""
        pass

    def update_or_create_lab(self):
        """Updates profiles and supporting list tables for projects lab module."""
        for profile_group_name, setup_items in self.lab_setup.iteritems():
            profile_group_models = site_lab_profiles.get_group_models(profile_group_name)
            aliquot_type_model = profile_group_models.get('aliquot_type')
            profile_model = profile_group_models.get('profile')
            profile_item_model = profile_group_models.get('profile_item')
            for item in setup_items.get('aliquot_type'):
                if aliquot_type_model.objects.filter(name=item.name):
                    aliquot_type = aliquot_type_model.objects.get(name=item.name)
                    aliquot_type.alpha_code = item.alpha_code
                    aliquot_type.numeric_code = item.numeric_code
                    aliquot_type.save()
                else:
                    aliquot_type_model.objects.create(name=item.name, alpha_code=item.alpha_code, numeric_code=item.numeric_code)
            # create profiles
            for item in setup_items.get('profile'):
                aliquot_type = aliquot_type_model.objects.get(alpha_code=item.alpha_code)
                if not profile_model.objects.filter(name=item.profile_name):
                    profile_model.objects.create(name=item.profile_name, aliquot_type=aliquot_type)
                else:
                    profile = profile_model.objects.get(name=item.profile_name)
                    profile.aliquot_type = aliquot_type
                    profile.save()
            # add profile items
            for item in setup_items.get('profile_item'):
                profile = profile_model.objects.get(name=item.profile_name)
                aliquot_type = aliquot_type_model.objects.get(alpha_code=item.alpha_code)
                if not profile_item_model.objects.filter(profile=profile, aliquot_type=aliquot_type):
                    profile_item_model.objects.create(profile=profile, aliquot_type=aliquot_type, volume=item.volume, count=item.count)
                else:
                    profile_item = profile_item_model.objects.get(profile=profile, aliquot_type=aliquot_type)
                    profile_item.volume = item.volume
                    profile_item.count = item.count
                    profile_item.save()

    def update_or_create_appointment_setup(self):
        """Updates configuration in the :mod:`appointment` module."""
        if Configuration.objects.all().count() == 0:
            Configuration.objects.create(**self.appointment_configuration)
        else:
            Configuration.objects.all().update(**self.appointment_configuration)

    def update_or_create_study_variables(self):
        """Updates configuration in the :mod:`bhp_variables` module."""
        if StudySpecific.objects.all().count() == 0:
            StudySpecific.objects.create(**self.study_variables_setup)
        else:
            StudySpecific.objects.all().update(**self.study_variables_setup)

        if self.study_site_setup and not StudySite.objects.filter(**self.study_site_setup).exists():
            StudySite.objects.create(**self.study_site_setup)
        if not Device().is_server() and StudySite.objects.all().count() > 1:
            raise ImproperlyConfigured('There has to be only one Study Site record on bhp_variables. Got {0}'.format(StudySite.objects.all().count()))

    def update_or_create_labeling(self):
        """Updates configuration in the :mod:`labeling` module."""
        for printer_setup in self.labeling.get('label_printer'):
            if LabelPrinter.objects.filter(cups_printer_name=printer_setup.cups_printer_name).count() == 0:
                LabelPrinter.objects.create(
                    cups_printer_name=printer_setup.cups_printer_name,
                    cups_server_ip=printer_setup.cups_server_ip,
                    default=printer_setup.default,
                    )
        else:
            label_printer = LabelPrinter.objects.get(cups_printer_name=printer_setup.cups_printer_name)
            label_printer.cups_server_ip = printer_setup.cups_server_ip
            label_printer.default = printer_setup.default

    def update_or_create_consent_catalogue(self):
        """Updates configuration in the :mod:`consent` module."""
        for catalogue_setup in self.consent_catalogue_list:
            catalogue_setup.update({'content_type_map': ContentTypeMap.objects.get(model=catalogue_setup.get('content_type_map').lower())})
            if not ConsentCatalogue.objects.filter(**catalogue_setup).exists():
                ConsentCatalogue.objects.create(**catalogue_setup)
            else:
                ConsentCatalogue.objects.filter(**catalogue_setup).update(**catalogue_setup)
