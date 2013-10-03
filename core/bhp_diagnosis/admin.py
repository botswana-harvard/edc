from django.contrib import admin
from bhp_common.models import MyModelAdmin
from models.code import Code
from models.organism import Organism
from models.site import Site


class CodeAdmin(MyModelAdmin):
    pass
admin.site.register(Code, CodeAdmin)


class OrganismAdmin(MyModelAdmin):
    pass
admin.site.register(Organism, OrganismAdmin)


class SiteAdmin(MyModelAdmin):
    pass
admin.site.register(Site, SiteAdmin)
