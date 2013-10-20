from .classes import section_index_view, site_sections

section_index_view.setup()
urlpatterns = []
for section_inst in site_sections.all().itervalues():
    section_inst.set_section_list(section_index_view.get_section_list())
    urlpatterns += section_inst.urlpatterns()
urlpatterns += section_index_view.urlpatterns()
