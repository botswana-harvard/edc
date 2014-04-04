from django.shortcuts import redirect
from edc.subject.appointment.models import Appointment
from edc.subject.entry.models.lab_entry import LabEntry
from edc.subject.entry.models.entry import Entry
from edc.entry_meta_data.models import RequisitionMetaData, ScheduledEntryMetaData


def additional_requisition(request):
    appointment_id = _get_param(request, 'appointment_id')
    lab_entry_id = _get_param(request, 'panel')

    appointment = Appointment.objects.get(pk=appointment_id)
    lab_entry = LabEntry.objects.get(pk=lab_entry_id)
    requisition_meta_data = RequisitionMetaData.objects.get(appointment=appointment, lab_entry=lab_entry)
    requisition_meta_data.entry_status = 'NEW'
    requisition_meta_data.save()

    dashboard_type = _get_param(request, 'dashboard_type')
    dashboard_model = _get_param(request, 'dashboard_model')
    dashboard_id = _get_param(request, 'dashboard_id')
    show = _get_param(request, 'show')
    url = _get_param(request, 'url')

    return redirect(url,
                    dashboard_type=dashboard_type,
                    dashboard_model=dashboard_model,
                    dashboard_id=dashboard_id,
                    show=show)


def _get_param(request, param_key):
    return request.GET[param_key]


def additional_entry_form(request):
    appointment_id = _get_param(request, 'appointment_id')
    entry_id = _get_param(request, 'entries')

    appointment = Appointment.objects.get(pk=appointment_id)
    entry = Entry.objects.get(pk=entry_id)
    entry_meta_data = ScheduledEntryMetaData.objects.get(appointment=appointment, entry=entry)
    entry_meta_data.entry_status = 'NEW'
    entry_meta_data.save()

    dashboard_type = _get_param(request, 'dashboard_type')
    dashboard_model = _get_param(request, 'dashboard_model')
    dashboard_id = _get_param(request, 'dashboard_id')
    show = _get_param(request, 'show')
    url = _get_param(request, 'url')

    return redirect(url,
                    dashboard_type=dashboard_type,
                    dashboard_model=dashboard_model,
                    dashboard_id=dashboard_id,
                    show=show)
