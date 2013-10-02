from django.contrib import messages
from lab_barcode.exceptions import PrinterException
from ph_dispenser.classes import DispensingLabel


def print_dispensing_label(modeladmin, request, dispensings):
    for dispensing in dispensings:
        model_label = DispensingLabel()
        try:
            model_label.print_label(
                request,
                dispensing,
                dispensing.copies,
                dispensing.identifier
                )
        except PrinterException as e:
            messages.add_message(request, messages.ERROR, e.value)


print_dispensing_label.short_description = "LABEL: print dispensing label"
