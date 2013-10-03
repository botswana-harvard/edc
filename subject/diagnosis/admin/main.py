from django.contrib import admin
from edc.base.admin.admin import BaseModelAdmin
from ..models import Code
from ..models import Organism
from ..models import Site


class CodeAdmin(BaseModelAdmin):
    pass
admin.site.register(Code, CodeAdmin)


class OrganismAdmin(BaseModelAdmin):
    pass
admin.site.register(Organism, OrganismAdmin)


class SiteAdmin(BaseModelAdmin):
    pass
admin.site.register(Site, SiteAdmin)
