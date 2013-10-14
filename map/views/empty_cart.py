from django.shortcuts import render_to_response
from django.template import RequestContext
from ..classes import site_mappers
from ..exceptions import MapperError


def empty_cart(request, message, **kwargs):
    """Empties cart.    """
    template = 'map_index.html'
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        mapper = site_mappers.get_registry(mapper_name)()
        try:
            del request.session['identifiers']
            del request.session['icon']
        except KeyError:
            pass
        return render_to_response(
                template, {
                    'mapper_name': mapper_name,
                    'regions': mapper.get_regions(),
                    'sections': mapper.get_sections(),
                    'icons': mapper.get_icons(),
                    'message': message,
                    'item_label': mapper.get_item_model_cls()._meta.object_name,
                    'region_label': mapper.get_region_label(),
                },
                context_instance=RequestContext(request)
            )
