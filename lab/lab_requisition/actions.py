from datetime import datetime

from django.contrib import messages

from lis.labeling.exceptions import PrinterException
from lis.exim.lab_export.classes import ExportDmis


def flag_as_received(modeladmin, request, queryset, **kwargs):
    """ Flags specimen(s) as received and generates a globally
    specimen identifier."""

    for qs in queryset:
        #if not qs.specimen_identifier:
        if qs.is_drawn.lower() == 'yes':
            qs.is_receive = True
            qs.is_receive_datetime = datetime.today()
            qs.save()
        else:
            mes = 'SubjectRequisition Id: \'{0}\' was not drawn, hence you cannot receive it.'.format(qs.requisition_identifier)
            messages.add_message(request, messages.ERROR, mes)
            break
            #raise forms.ValidationError('Subject requisition \'{0}\' was not drawn, hence you cannot receive it.'.format(qs.requisition_identifier))

flag_as_received.short_description = "RECEIVE as received against requisition"


def flag_as_not_received(modeladmin, request, queryset):

    for qs in queryset:
        qs.is_receive = False
        qs.is_receive_datetime = datetime.today()
        qs.save()
flag_as_not_received.short_description = "UN-RECEIVE: flag as NOT received"


def flag_as_not_labelled(modeladmin, request, queryset):
    for qs in queryset:
        qs.is_labelled = False
        qs.save()

flag_as_not_labelled.short_description = "UN-LABEL: flag as NOT labelled"


def receive_on_dmis(modeladmin, request, queryset):
    export_dmis = ExportDmis()
    for qs in queryset:
        qs.comment, qs.is_lis = export_dmis.receive(qs)
        qs.save()
flag_as_not_labelled.short_description = "DMIS-receive: receive sample on the dmis (for BHHRL LAB STAFF ONLY)"


def print_requisition_label(modeladmin, request, requisitions):
    """ Prints a specimen label for a received specimen using the :func:`print_label`
    method attached to the requisition model.
    
    Requisitions must be 'received' before a label can be printed."""
    try:
        for requisition in requisitions:
            if requisition.is_receive:
                requisition.print_label(request)
            else:
                messages.add_message(request, messages.ERROR,
                                     'Requisition {0} has not been received. Labels '
                                     'cannot be printed until the specimen is '
                                     'received.'.format(requisition.requisition_identifier,))
    except PrinterException as e:
        messages.add_message(request, messages.ERROR, e.value)

print_requisition_label.short_description = "LABEL: print requisition label"
