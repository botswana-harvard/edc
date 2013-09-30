

def set_is_dispatched(modeladmin, request, queryset, **kwargs):
    """Sets is dispatched to True"""
    for qs in queryset:
        if qs.is_dispatched == False:
            qs.is_dispatched = True
            qs.return_datetime = None
            qs.save()
set_is_dispatched.short_description = "Set is_dispatched to True."
