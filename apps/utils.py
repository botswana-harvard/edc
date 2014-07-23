from django.conf import settings


class Conf(object):

    @staticmethod
    def get(key, return_exception=False):
        try:
            return getattr(settings, key)
        except AttributeError:
            if return_exception:
                raise AttributeError('The settings file has no attribute: "{}"'.format(key))
            return None

    @staticmethod
    def return_site_name():
        from map.classes import site_mappers
        mapper = None
        mapper = site_mappers.get_registry(site_mappers.get_current_mapper().map_area)()
        if mapper:
            site_name = mapper.get_map_area()
        else:
            site_name = 'NO_MAPPER'
        return site_name