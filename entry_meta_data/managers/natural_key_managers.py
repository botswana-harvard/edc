from django.db import models


class NaturalKeyRequisitionMetaDataManager():

    def get_by_natural_key(self, visit_instance, visit_definition_code, subject_identifier_as_pk, code2, name):
        Appointment = models.get_model('appointment', 'Appointment')
        LabEntry = models.get_model('entry_meta_data', 'ScheduledEntryMetaData')
        appointment = Appointment.objects.get_by_natural_key(visit_instance, visit_definition_code, subject_identifier_as_pk)
        lab_entry = LabEntry.objects.get_by_natural_key(visit_definition_code, name)
        return self.get(appointment=appointment, lab_entry=lab_entry)


class NaturalKeyEntryMetaDataManager():

    def get_by_natural_key(self, visit_instance, visit_definition_code, subject_identifier_as_pk, code2, app_label, model):
        Appointment = models.get_model('appointment', 'Appointment')
        Entry = models.get_model('entry_meta_data', 'ScheduledEntryMetaData')
        appointment = Appointment.objects.get_by_natural_key(visit_instance, visit_definition_code, subject_identifier_as_pk)
        entry = Entry.objects.get_by_natural_key(visit_definition_code, app_label, model)
        return self.get(appointment=appointment, entry=entry)