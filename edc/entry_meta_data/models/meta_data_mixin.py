from edc.subject.entry.models import Entry, LabEntry
from edc.subject.appointment.models import Appointment
from edc_constants.constants import REQUIRED, NOT_REQUIRED, KEYED

from .scheduled_entry_meta_data import ScheduledEntryMetaData
from .requisition_meta_data import RequisitionMetaData


class MetaDataMixin(object):

    """Class to manipulate meta data for forms and requisitions."""

    def form_is_required(self, appointment, app_label, model_name, message=None, create=None):
        """Saves the entry_status as REQUIRED."""
        self._change_form_entry_status(REQUIRED, appointment, app_label, model_name, message, create)

    def form_is_not_required(self, appointment, app_label, model_name, message=None):
        """Saves the entry_status as REQUIRED."""
        self._change_form_entry_status(NOT_REQUIRED, appointment, app_label, model_name, message)

    def requisition_is_required(self, appointment, app_label, model_name, panel_name, message=None):
        self._change_requisition_entry_status(
            REQUIRED, appointment, app_label, model_name, panel_name, message)

    def requisition_is_not_required(self, appointment, app_label, model_name, panel_name, message=None):
        self._change_requisition_entry_status(
            NOT_REQUIRED, appointment, app_label, model_name, panel_name, message)

    def change_to_off_study_visit(self, appointment, off_study_app_label, off_study_model_name, message=None):
        """Changes the meta data so that only the off study form is required.

        * if the off study form does not exist it will be created.
        * if a form is already KEYED it will not be changed.
        """
        self._change_all_to_not_required(appointment)
        self.form_is_required(self, appointment, off_study_app_label, off_study_model_name, message, create=True)

    def change_to_death_visit(self, appointment, app_label, off_study_model_name, death_model_name, message=None):
        """Changes the meta data so that only the death and off study forms are required.

        If either form does not exist they will be created."""
        self.change_to_off_study_visit(appointment, app_label, off_study_model_name, message)
        self.form_is_required(self, appointment, app_label, death_model_name, message, create=True)

    def change_to_unscheduled_visit(self, appointment, off_study_app_label, off_study_model_name, message=None):
        """Changes all meta data to not required."""
        self._change_all_to_not_required(appointment)

    def _change_all_to_not_required(self, appointment):
        """Changes all meta data to not required."""
        base_appointment = self.get_base_appointment(appointment)
        ScheduledEntryMetaData.objects.filter(
            appointment=base_appointment,
            registered_subject=appointment.registered_subject).exclude(
                entry_status__in=[NOT_REQUIRED, KEYED]).update(
                entry_status=NOT_REQUIRED)
        RequisitionMetaData.objects.filter(
            appointment=base_appointment,
            registered_subject=appointment.registered_subject).exclude(
                entry_status__in=[NOT_REQUIRED, KEYED]).update(
                entry_status=NOT_REQUIRED)

    def _change_form_entry_status(self, entry_status, appointment, app_label, model_name, message=None, create=None):
        """Changes a form's entry status.

        Raises an error if the form does not exist unless 'create' is True. Except for OFF STUDY
        there should not be a need to create a form."""
        try:
            base_appointment = self.get_base_appointment(appointment)
            scheduled_entry_meta_data = ScheduledEntryMetaData.objects.get(
                entry__app_label=app_label,
                entry__model_name=model_name,
                appointment=base_appointment
            )
        except ScheduledEntryMetaData.DoesNotExist as e:
            if create:
                scheduled_entry_meta_data = self._create_form(appointment, app_label, model_name)
            else:
                message = message or ''
                raise ScheduledEntryMetaData.DoesNotExist(
                    '{} {}.{} {}'.format(str(e), app_label, model_name, message))
        self._change_entry_status(scheduled_entry_meta_data, entry_status)

    def _change_requisition_entry_status(
            self, entry_status, appointment, app_label, model_name, panel_name, message=None, create=None):
        """Changes a requisition's entry status.

        Raises an error if the requisition does not exist unless 'create' is True."""
        try:
            base_appointment = self.get_base_appointment(appointment)
            requisition_meta_data = RequisitionMetaData.objects.get(
                lab_entry__app_label=app_label,
                lab_entry__model_name=model_name,
                appointment=base_appointment,
                lab_entry__requisition_panel__name=panel_name
            )
        except RequisitionMetaData.DoesNotExist as e:
            if create:
                requisition_meta_data = self._create_form(appointment, app_label, model_name)
            else:
                message = message or ''
                raise RequisitionMetaData.DoesNotExist(
                    '{} {}.{}.{} {}'.format(str(e), app_label, model_name, panel_name, message))
        self._change_entry_status(requisition_meta_data, entry_status)

    def _change_entry_status(self, meta_data, entry_status):
        """Changes the entry_status if not already set to the given value."""
        if meta_data.entry_status != entry_status:
            meta_data.entry_status = entry_status
            meta_data.save()

    def _create_form(self, appointment, app_label, model_name):
        """Creates a form with entry status set to REQUIRED."""
        base_appointment = self.get_base_appointment(appointment)
        entry = Entry.objects.get(
            app_label=app_label,
            model_name=model_name,
            visit_definition=base_appointment.visit_definition)
        scheduled_entry_meta_data = ScheduledEntryMetaData.objects.create(
            entry=entry,
            appointment=base_appointment,
            entry_status=REQUIRED)
        return scheduled_entry_meta_data

    def _create_requisition(self, appointment, app_label, model_name, panel_name):
        """Creates a requisition with entry status set to REQUIRED."""
        base_appointment = self.get_base_appointment(appointment)
        lab_entry = LabEntry.objects.get(
            model_name=model_name,
            requisition_panel=panel_name,
            visit_definition=base_appointment.visit_definition)
        requisition_meta_data = RequisitionMetaData.objects.create(
            lab_entry=lab_entry,
            appointment=base_appointment,
            lab_entry__requisition_panel__name=panel_name)
        return requisition_meta_data

    def get_base_appointment(self, appointment):
        """Returns the base appointment (CODE.0) or the given appointment if it is the base.

        Mode than one appointments may span for a given visit code. The appointments are incremented
        using a decimal, e.g. 1000.0, 1000.1, 1000.2 , etc. 1000.0 is the "base" appointment."""
        if appointment.visit_instance != '0':
            appointment = Appointment.objects.get(
                registered_subject=appointment.registered_subject,
                visit_instance='0', visit_definition=appointment.visit_definition)
        return appointment

#     def remove_scheduled_requisition(self, lab_meta_data):
#         # Ensure there are no keyed forms
#         for meta_data in lab_meta_data:
#             if meta_data.entry_status == KEYED:
#                 return False
#         lab_meta_data.delete()
#         return True
# 
#     def lab_entry_model_options(self, model_name, panel_name):
#         model_options = {}
#         model_options.update()
#         return model_options
# 
#     def query_entry(self, model_name, visit_definition):
#         try:
#             return Entry.objects.get(model_name=model_name, visit_definition=visit_definition)
#         except Entry.DoesNotExist:
#             return False
# 
#     def create_scheduled_meta_data(self, appointment, entry, registered_subject):
#         appointment = self.check_instance(appointment)
#         scheduled_meta_data = self.query_scheduled_meta_data(appointment, entry, registered_subject)
#         if not scheduled_meta_data:
#             scheduled_meta_data = ScheduledEntryMetaData.objects.create(
#                 appointment=appointment, entry=entry, registered_subject=registered_subject
#             )
#         scheduled_meta_data.entry_status = NEW
#         scheduled_meta_data.save()
#         return scheduled_meta_data
# 
#     def lab_entry(self, model_name, panel, visit_definition):
#         return LabEntry.objects.get(model_name=model_name, requisition_panel=panel, visit_definition=visit_definition)
# 
#     def requisition_meta_data(self, appointment, lab_entry, registered_subject):
#         requisition_meta_data = RequisitionMetaData.objects.filter(
#             appointment=appointment, lab_entry=lab_entry, registered_subject=registered_subject
#         )
#         if requisition_meta_data.count() == 1:
#             return requisition_meta_data[0]
#         return requisition_meta_data
# 
#     def create_requisition_meta_data(self, appointment, lab_entry, registered_subject):
#         requisition_meta_data = self.query_requisition_meta_data(appointment, lab_entry, registered_subject)
#         if not requisition_meta_data:
#             requisition_meta_data = RequisitionMetaData.objects.create(
#                 appointment=appointment, lab_entry=lab_entry, registered_subject=registered_subject)
#         requisition_meta_data.entry_status = NEW
#         requisition_meta_data.save()
#         return requisition_meta_data
# 
#     def remove_all_meta_data(self, appointment, registered_subject, scheduled_meta_data, requisition_meta_data):
#         flag = False
#         # Ensure there are no keyed forms
#         for meta_data in scheduled_meta_data:
#             if meta_data.entry_status == KEYED:
#                 flag = True
#         # Ensure there are no keyed lab requisitions
#         for rmeta_data in requisition_meta_data:
#             if rmeta_data.entry_status == KEYED:
#                 flag = True
#         if not flag:
#             scheduled_meta_data.delete()
#             requisition_meta_data.delete()
#             return True
#         else:
#             return False
#
