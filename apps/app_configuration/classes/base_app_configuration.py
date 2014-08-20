import json

from django.db.models import get_model

from edc.core.bhp_content_type_map.classes import ContentTypeMapHelper
from edc.core.bhp_content_type_map.models import ContentTypeMap
from edc.core.bhp_variables.models import StudySpecific, StudySite
from edc.export.models import ExportPlan
from edc.lab.lab_clinic_api.models import AliquotType, Panel
from edc.lab.lab_profile.classes import site_lab_profiles
from edc.notification.models import NotificationPlan
from edc.subject.appointment.models import Holiday
from edc.subject.consent.models import ConsentCatalogue
from edc.subject.entry.models import RequisitionPanel
from edc.utils import datatype_to_string

from lis.labeling.models import LabelPrinter
from lis.labeling.models import ZplTemplate

from .defaults import default_global_configuration
from ..models import GlobalConfiguration


class BaseAppConfiguration(object):

    appointment_configuration = None
    consent_catalogue_list = None
    consent_catalogue_setup = None
    lab_clinic_api_setup = None
    lab_setup = None
    study_site_setup = None
    study_variables_setup = None
    export_plan_setup = {}
    notification_plan_setup = {}
    labeling_setup = {}

    def __init__(self):
        """Updates content type maps then runs each configuration method with the corresponding class attribute.

        Configuration methods update default data in supporting tables."""
        ContentTypeMapHelper().populate()
        ContentTypeMapHelper().sync()
        self.update_global()
        self.update_or_create_study_variables()
        self.update_or_create_consent_catalogue()
        self.update_or_create_lab_clinic_api()
        self.update_or_create_lab()
        self.update_or_create_labeling()
        self.update_export_plan_setup()
        self.update_notification_plan_setup()
        self.update_holidays_setup()

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

    def update_or_create_study_variables(self):
        """Updates configuration in the :mod:`bhp_variables` module."""
        if StudySpecific.objects.all().count() == 0:
            StudySpecific.objects.create(**self.study_variables_setup)
        else:
            specifics = StudySpecific.objects.all()
            specifics.update(**self.study_variables_setup)
            for sp in specifics:
                # This extra step is required so that signals can fire. Queryset .update() does to fire any signals.
                sp.save()
        if not StudySite.objects.filter(site_code=self.study_site_setup.get('site_code')).exists():
            StudySite.objects.create(**self.study_site_setup)

    def update_or_create_labeling(self):
        """Updates configuration in the :mod:`labeling` module."""

        for printer_setup in self.labeling_setup.get('label_printer', []):
            try:
                label_printer = LabelPrinter.objects.get(cups_printer_name=printer_setup.cups_printer_name)
                label_printer.cups_server_ip = printer_setup.cups_server_ip
                label_printer.default = printer_setup.default
                label_printer.save()
            except LabelPrinter.DoesNotExist:
                LabelPrinter.objects.create(
                    cups_printer_name=printer_setup.cups_printer_name,
                    cups_server_ip=printer_setup.cups_server_ip,
                    default=printer_setup.default,
                )
        for zpl_template_setup in self.labeling_setup.get('zpl_template', []):
            try:
                zpl_template = ZplTemplate.objects.get(name=zpl_template_setup.name)
                zpl_template.template = zpl_template_setup.template
                zpl_template.default = zpl_template_setup.default
                zpl_template.save()
            except ZplTemplate.DoesNotExist:
                ZplTemplate.objects.create(
                    name=zpl_template_setup.name,
                    template=zpl_template_setup.template,
                    default=zpl_template_setup.default,
                )

    def update_or_create_consent_catalogue(self):
        """Updates configuration in the :mod:`consent` module."""
        for catalogue_setup in self.consent_catalogue_list:
            content_type_map_string = catalogue_setup.get('content_type_map')
            catalogue_setup.update({'content_type_map': ContentTypeMap.objects.get(model=catalogue_setup.get('content_type_map'))})
            if not ConsentCatalogue.objects.filter(**catalogue_setup).exists():
                ConsentCatalogue.objects.create(**catalogue_setup)
            else:
                catalogues = ConsentCatalogue.objects.filter(**catalogue_setup)
                catalogues.update(**catalogue_setup)
                for ct in catalogues:
                    # This extra step is required so that signals can fire. Queryset .update() does to fire any signals.
                    ct.save()
            catalogue_setup.update({'content_type_map': content_type_map_string})

    def update_global(self):
        """Creates or updates global configuration options in app_configuration.

        First ensures defaults exist, then, if user specification exists, overwrites the defaults or adds new."""
        configurations = [default_global_configuration]
        try:
            configurations.append(self.global_configuration)
        except AttributeError:
            pass   # maybe attribute does not exist
        for configuration in configurations:
            for category_name, category_configuration in configuration.iteritems():
                for attr, value in category_configuration.iteritems():
                    string_value = datatype_to_string(value)
                    string_value = string_value.strip(' "')
                    try:
                        global_configuration = GlobalConfiguration.objects.get(attribute=attr)
                        global_configuration.value = string_value
                        global_configuration.save()
                    except GlobalConfiguration.DoesNotExist:
                        GlobalConfiguration.objects.create(category=category_name, attribute=attr, value=string_value)

    def update_export_plan_setup(self):
        if self.export_plan_setup:
            for model_config, export_plan in self.export_plan_setup.iteritems():
                app_label, model_name = model_config.split('.')
                model = get_model(app_label, model_name)
                try:
                    export_plan_instance = ExportPlan.objects.get(app_label=model._meta.app_label, object_name=model._meta.object_name)
                    export_plan_instance.fields = json.dumps(export_plan.get('fields'))
                    export_plan_instance.extra_fields = json.dumps(export_plan.get('extra_fields'))
                    export_plan_instance.exclude = json.dumps(export_plan.get('exclude'))
                    export_plan_instance.header = export_plan.get('header')
                    export_plan_instance.track_history = export_plan.get('track_history')
                    export_plan_instance.show_all_fields = export_plan.get('show_all_fields')
                    export_plan_instance.delimiter = export_plan.get('delimiter')
                    export_plan_instance.encrypt = export_plan.get('encrypt')
                    export_plan_instance.strip = export_plan.get('strip')
                    export_plan_instance.target_path = export_plan.get('target_path')
                    export_plan_instance.notification_plan_name = export_plan.get('notification_plan_name')
                    export_plan_instance.save()
                except ExportPlan.DoesNotExist:
                    ExportPlan.objects.create(
                        app_label=model._meta.app_label,
                        object_name=model._meta.object_name,
                        fields=json.dumps(export_plan.get('fields')),
                        extra_fields=json.dumps(export_plan.get('extra_fields')),
                        exclude=json.dumps(export_plan.get('exclude')),
                        header=export_plan.get('header'),
                        track_history=export_plan.get('track_history'),
                        show_all_fields=export_plan.get('show_all_fields'),
                        delimiter=export_plan.get('delimiter'),
                        encrypt=export_plan.get('encrypt'),
                        strip=export_plan.get('strip'),
                        target_path=export_plan.get('target_path'),
                        notification_plan_name=export_plan.get('notification_plan_name'),
                    )

    def update_notification_plan_setup(self):
        if self.notification_plan_setup:
            for notification_plan_name, notification_plan in self.notification_plan_setup.iteritems():
                try:
                    notification_plan_instance = NotificationPlan.objects.get(name=notification_plan_name)
                    notification_plan_instance.name = notification_plan.get('name')
                    notification_plan_instance.friendly_name = notification_plan.get('friendly_name')
                    notification_plan_instance.subject_format = notification_plan.get('subject_format')
                    notification_plan_instance.body_format = notification_plan.get('body_format')
                    notification_plan_instance.recipient_list = json.dumps(notification_plan.get('recipient_list'))
                    notification_plan_instance.cc_list = json.dumps(notification_plan.get('cc_list'))
                    notification_plan_instance.save()
                except NotificationPlan.DoesNotExist:
                    NotificationPlan.objects.create(
                        name=notification_plan.get('name'),
                        friendly_name=notification_plan.get('friendly_name'),
                        subject_format=notification_plan.get('subject_format'),
                        body_format=notification_plan.get('body_format'),
                        cc_list=json.dumps(notification_plan.get('cc_list')),
                        )

    def update_holidays_setup(self):
        """Updates holiday configurations in appointment__holiday module."""
        for holiday in self.holidays_setup:
            if not Holiday.objects.filter(holiday_name=holiday).exists():
                Holiday.objects.create(holiday_name=holiday, holiday_date=self.holidays_setup.get(holiday))
            else:
                updated_holiday = Holiday.objects.get(holiday_name=holiday)
                updated_holiday.holiday_date = self.holidays_setup.get(holiday)
                updated_holiday.save()
