# Import django modules
from django.shortcuts import render_to_response
from django.template import RequestContext
from bhp_map.classes import site_mappers
from bhp_map.exceptions import MapperError


def map_section(request, **kwargs):
    """Select ward and section to separate items into section in a ward

    The selected ward and section are going to be use to set a section for the ward selected.

   """
    template = 'map_section.html'
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        m = site_mappers.get_registry(mapper_name)()
        cart_size = 0
        identifiers = []
        icon = request.session.get('icon', None)
        if 'identifiers' in request.session:
            cart_size = len(request.session['identifiers'])
            identifiers = request.session['identifiers']
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'regions': m.get_regions(),
                    'icons': m.get_icons(),
                    'item_region_field': m.get_region_field_attr(),
                    'region_label': m.get_region_label(),
                    'session_icon': icon,
                    'cart_size': cart_size,
                    'identifiers': identifiers,
                    'region_field_attr': m.get_region_field_attr(),
                    'section_field_attr': m.get_section_field_attr(),
                    'show_map': 1,
                    'has_items': True,
                    'option': 'plot'
                },
                context_instance=RequestContext(request))
