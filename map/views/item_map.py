from operator import itemgetter
from collections import OrderedDict
from django.conf import settings
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.db.models import Q
from ..classes import site_mappers
from ..exceptions import MapperError


def item_map(request, **kwargs):
    """Displays map for a subject on the dashboard

    Show the location visually on the map of a subject from the dash by clicking the view map button on the dashboard
    """
    mapper_name = kwargs.get('mapper_name', '')
    if not site_mappers.get_registry(mapper_name):
        raise MapperError('Mapper class \'{0}\' is not registered.'.format(mapper_name))
    else:
        m = site_mappers.get_registry(mapper_name)()
        longitude = kwargs.get('lon', None)
        latitude = kwargs.get('lat', None)
        map = None
        if not longitude:
            raise MapperError('Attribute longitude may not be None. Got {0}'.format(kwargs))
        if not latitude:
            raise MapperError('Attribute latitude may not be None. Got {0}'.format(kwargs))
        identifier = kwargs.get('identifier', None)
        item = m.get_item_model_cls().objects.filter(Q(**{m.get_identifier_field_attr(): identifier}))
        item_map = getattr(item[0], m.map_field_attr) 
        folder = settings.MEDIA_ROOT
        landmark_list = []
        landmarks = m.get_landmarks()
        letters = ["A", "B", "C", "D", "E", "F", "G", "H", "I", "J", "K", "L", "M", "N",
                    "O", "Q", "R", "S", "T", "U", "V", "W", "X", "Y", "Z"]
        
        for place, lon, lat in landmarks:
            landmark_list.append([place, lon, lat])
        lat = getattr(item[0], m.target_gps_lat_field_attr)
        lon = getattr(item[0], m.target_gps_lon_field_attr)
        lmarks = []
        map = request.GET.get('map')
        for mark in landmark_list:
            dist = m.gps_distance_between_points(lat, lon, mark[1], mark[2])
            lmarks.append([dist, mark[0]])
        lmark = sorted(lmarks,key=itemgetter(0))
        markers_l = {}
        count = 0
        for distanace, p_point in lmark:
            if count < 3:
                markers_l[letters[count]]=p_point
                count +=1
        return render_to_response(
                'item_map_location.html', {
                    'lat': latitude,
                    'mapper_name': mapper_name,
                    'lon': longitude,
                    'landmarks': landmark_list,
                    'identifier': identifier,
                    'folder': folder,
                    'MEDIA-ROOT': settings.MEDIA_ROOT,
                    'item_map': item_map,
                    'markers_l': markers_l,
                    'map': map,
                },
                context_instance=RequestContext(request)
            )
