from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from ..models import DiagnosisCode
from ..models import DiagnosisOrganism
from ..models import DiagnosisSite


class CodeAdmin(BaseModelAdmin):
    pass
admin.site.register(DiagnosisCode, CodeAdmin)


class OrganismAdmin(BaseModelAdmin):
    pass
admin.site.register(DiagnosisOrganism, OrganismAdmin)


class SiteAdmin(BaseModelAdmin):
    pass
admin.site.register(DiagnosisSite, SiteAdmin)
