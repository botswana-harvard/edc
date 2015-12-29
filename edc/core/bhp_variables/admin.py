from django.contrib import admin

from .forms import StudySpecificForm
from .models import StudySpecific


class StudySpecificAdmin(admin.ModelAdmin):

    form = StudySpecificForm

    list_display = (
        "protocol_number",
        "protocol_code",
        "study_start_datetime",
        "machine_type",
        "hostname_prefix",
        "device_id")

admin.site.register(StudySpecific, StudySpecificAdmin)
