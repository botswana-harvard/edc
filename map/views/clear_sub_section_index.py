from django.shortcuts import render_to_response
from django.template import RequestContext
from ..exceptions import MapperError
from ..classes import site_mappers


def clear_sub_section_index(request, **kwargs):
    """Clears all sections for a given region."""

    template = 'clear_sub_section_index.html'
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' does is not registered.'.format(mapper_name))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'item_label': mapper.get_item_label(),
                    'section_label': mapper.get_section_label(),
                    'region_label': '{0}s'.format(mapper.get_region_label()),
                    'regions': mapper.get_regions(),
                    'sections': mapper.get_sections(),
                    'region_field_attr': mapper.get_region_field_attr(),
                    'section_field_attr': mapper.get_section_field_attr(),
                 },
                context_instance=RequestContext(request)
            )
