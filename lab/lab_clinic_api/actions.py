from django.contrib import messages

from lis.labeling.exceptions import PrinterException

from .classes import SpecimenHelper
from .models import Result, ResultItem, Order


def recalculate_grading(modeladmin, request, queryset):

    for n, qs in enumerate(queryset):
        if isinstance(qs, Result):
            for result_item in ResultItem.objects.filter(result=qs):
                result_item.save()
        elif isinstance(qs, ResultItem):
            qs.save()
        else:
            modeladmin.message_user(request, 'Nothing to do. Must be either a result or result item.')
            break
    modeladmin.message_user(request, 'Recalculated grading and references for {0} items.'.format(n))

recalculate_grading.short_description = "Recalculate grading and references"


def flag_as_reviewed(modeladmin, request, queryset):
        for qs in queryset:
            if not isinstance(qs, Result):
                modeladmin.message_user(request, 'To review results, go to the results section.')
                break
            qs.reviewed = True
            if not qs.review:
                qs.save()
            qs.review.review_status = 'REVIEWED'
            qs.review.save()
            qs.save()
flag_as_reviewed.short_description = "Review: flag as reviewed"


def unflag_as_reviewed(modeladmin, request, queryset):
        for qs in queryset:
            if not isinstance(qs, Result):
                modeladmin.message_user(request, 'To review results, go to the results section.')
                break
            qs.reviewed = False
            if not qs.review:
                qs.save()
            qs.review.review_status = 'REQUIRES_REVIEWED'
            qs.review.save()
            qs.save()
unflag_as_reviewed.short_description = "Review: flag as NOT reviewed"


def refresh_order_status(modeladmin, request, queryset):
        updated = 0
        tot = 0
        for qs in queryset:
            if isinstance(qs, Order):
                tot += 1
                status = qs.get_status()
                if status != qs.status:
                    qs.save()
                    updated += 1
        if tot == 0:
            modeladmin.message_user(request, 'Nothing to do. Must be a selection of Orders.')
        else:
            modeladmin.message_user(request, 'Checked status on {0} orders. - updated {1}.'.format(tot, updated))
refresh_order_status.short_description = "Orders: refresh status"


def print_aliquot_label(modeladmin, request, aliquots):
    """ Prints a specimen label for a received specimen using the :func:`print_label`
    method attached to the requisition model."""
    specimen_helper = SpecimenHelper()
    try:
        for aliquot in aliquots:
            specimen_helper.print_aliquot_label(request, aliquot)
    except PrinterException as e:
        messages.add_message(request, messages.ERROR, e.value)

print_aliquot_label.short_description = "LABEL: print aliquot label"
