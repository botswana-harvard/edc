from dateutil import parser

from django.utils.encoding import force_text

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.models import StudySpecific, StudySite
from edc.lab.lab_clinic_api.models import AliquotType, Panel
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.subject.appointment.models import Configuration
from edc.subject.consent.models import ConsentCatalogue
from edc.subject.entry.models import RequisitionPanel

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
        self.update_global()
        self.update_or_create_appointment_setup()
        self.update_or_create_study_variables()
        self.update_or_create_consent_catalogue()
        self.update_or_create_lab_clinic_api()
        self.update_or_create_lab()
        self.update_or_create_labeling()

    def update_or_create_lab_clinic_api(self):
        """Configure lab clinic api list models."""
        for item in self.lab_clinic_api_setup.get('aliquot_type'):
            if AliquotType.objects.filter(name=item.name):
                aliquot_type = AliquotType.objects.get(name=item.name)
                aliquot_type.alpha_code = item.alpha_code
                aliquot_type.numeric_code = item.numeric_code
                aliquot_type.save()
            else:
                AliquotType.objects.create(
                    name=item.name,
                    alpha_code=item.alpha_code,
                    numeric_code=item.numeric_code)
        # update / create panels
        for item in self.lab_clinic_api_setup.get('panel'):
            if Panel.objects.filter(name=item.name):
                panel = Panel.objects.get(name=item.name)
                panel.panel_type = item.panel_type
                panel.save()
            else:
                panel = Panel.objects.create(name=item.name, panel_type=item.panel_type)
            # add aliquots to panel
            panel.aliquot_type.clear()
            aliquot_type = AliquotType.objects.get(alpha_code=item.aliquot_type_alpha_code)
            panel.aliquot_type.add(aliquot_type)

    def update_or_create_lab(self):
        """Updates profiles and supporting list tables for site specific lab module (e.g. bcpp_lab, mpepu_lab, ...).

        The supporting model classes Panel, AliquotType, Profile and ProfileItem
        are fetched from the global site_lab_profiles."""

        for setup_items in self.lab_setup.itervalues():
            aliquot_type_model = site_lab_profiles.group_models.get('aliquot_type')
            panel_model = site_lab_profiles.group_models.get('panel')
            profile_model = site_lab_profiles.group_models.get('profile')
            profile_item_model = site_lab_profiles.group_models.get('profile_item')
            # update / create aliquot_types
            for item in setup_items.get('aliquot_type'):
                if aliquot_type_model.objects.filter(name=item.name):
                    aliquot_type = aliquot_type_model.objects.get(name=item.name)
                    aliquot_type.alpha_code = item.alpha_code
                    aliquot_type.numeric_code = item.numeric_code
                    aliquot_type.save()
                else:
                    aliquot_type_model.objects.create(name=item.name, alpha_code=item.alpha_code, numeric_code=item.numeric_code)
            # update / create panels
            for item in setup_items.get('panel'):
                if panel_model.objects.filter(name=item.name):
                    panel = panel_model.objects.get(name=item.name)
                    panel.panel_type = item.panel_type
                    panel.save()
                else:
                    panel = panel_model.objects.create(name=item.name, panel_type=item.panel_type)
                # add aliquots to panel
                panel.aliquot_type.clear()
                aliquot_type = aliquot_type_model.objects.get(alpha_code=item.aliquot_type_alpha_code)
                panel.aliquot_type.add(aliquot_type)
                # create lab entry requisition panels based on this panel info
                if RequisitionPanel.objects.filter(name=item.name):
                    requisition_panel = RequisitionPanel.objects.get(name=item.name)
                    requisition_panel.aliquot_type_alpha_code = item.aliquot_type_alpha_code
                    requisition_panel.save()
                else:
                    requisition_panel = RequisitionPanel.objects.create(name=item.name, aliquot_type_alpha_code=item.aliquot_type_alpha_code)
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
        if not StudySite.objects.filter(site_code=self.study_site_setup.get('site_code')).exists():
            StudySite.objects.create(**self.study_site_setup)

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
            content_type_map_string = catalogue_setup.get('content_type_map')
            catalogue_setup.update({'content_type_map': ContentTypeMap.objects.get(model=catalogue_setup.get('content_type_map').lower())})
            if not ConsentCatalogue.objects.filter(**catalogue_setup).exists():
                ConsentCatalogue.objects.create(**catalogue_setup)
            else:
                ConsentCatalogue.objects.filter(**catalogue_setup).update(**catalogue_setup)
            catalogue_setup.update({'content_type_map': content_type_map_string})

    def update_global(self):
        """Creates or updates global configuration options in app_configuration.

        First ensures defaults exist, then, if user specification exists, overwrites the defaults or adds new."""
        default_configuration = {'dashboard': {'show_not_required_metadata': True, 'allow_additional_requisitions': False}}
        configurations = [default_configuration]
        try:
            configurations.append(self.global_configuration)
        except AttributeError:
            pass   # maybe attribute does not exist
        for configuration in configurations:
            for category_name, category_configuration in configuration.iteritems():
                for attr, value in category_configuration.iteritems():
                    if value == True:  # store booleans, None as a text string
                        string_value = 'True'
                    if value == False:
                        string_value = 'False'
                    if value == None:
                        string_value = 'None'
                    try:
                        configuration = Configuration.objects.get_attr_value(attribute=attr).value = string_value
                        configuration.save()
                    except:
                        try:
                            string_value = value.strftime('%Y-%m-%d')
                            if not parser.parse(string_value) == value:
                                raise ValueError
                        except ValueError:
                            pass
                        try:
                            string_value = value.strftime('%Y-%m-%d %H:%M')
                            if not parser.parse(string_value) == value:
                                raise ValueError
                        except ValueError:
                            pass
                        string_value = force_text(value)
                        Configuration.objects.create(category=category_name, attribute=attr, value=string_value)
