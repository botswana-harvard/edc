import copy

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

from ..exceptions import MapperError

from .mapper import Mapper


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class Controller(object):

    """ Main controller of :class:`Mapping` objects. """

    def __init__(self):
        self._registry = {}
        self.autodiscovered = False

    def set_registry(self, mapper_cls):
        """Registers a given mapper class to the site registry."""
        if not issubclass(mapper_cls, Mapper):
            raise MapperError('Expected a subclass of Mapper.')
        # use map_area class attribute add the dictionary key
        if mapper_cls.map_area in self._registry:
            raise AlreadyRegistered('The mapper class {0} is already registered ({1})'.format(mapper_cls, mapper_cls.map_area))
        self._registry[mapper_cls.map_area] = mapper_cls

    def get(self, name):
        """Returns a key, value pair from the dictionary for the given key."""
        return self._registry.get(name)

    def get_registry(self, name=None):
        """Returns the site mapper registry dictionary."""
        if name:
            if name in self._registry:
                return self._registry.get(name)
            else:
                raise MapperError('{0} is not a valid mapper name in {1}.'.format(name, self._registry))
        return self._registry

    def get_as_list(self):
        """Returns a list of dictionary keys from the registry dictionary to be used as a list of map areas or communities."""
        lst = [k for k in self._registry]
        lst.sort()
        return lst

    def get_current_mapper(self):
        """Returns the mapper for the current community using the settings attribute CURRENT_COMMUNITY as a key.

        If CURRENT_COMMUNITY_CHECK is set to True or is not set, the value of CURRENT_COMMUNITY will be checked
        against plot information before returning the mapper."""
        try:
            community_check = settings.CURRENT_COMMUNITY_CHECK
        except AttributeError:
            community_check = True
        if community_check:
            if 'CURRENT_COMMUNITY' not in dir(settings) or not settings.CURRENT_COMMUNITY:
                raise MapperError('Ensure settings.CURRENT_COMMUNITY exists and is not \'None\'.')
            if not settings.DEVICE_ID == '99':
                mapper_class = self.get_registry(settings.CURRENT_COMMUNITY)()
                items = mapper_class.get_item_model_cls().objects.all()
                if items:
                    if items and not getattr(items[0], mapper_class.map_area_field_attr) == settings.CURRENT_COMMUNITY:
                        raise MapperError('The settings current community does not match the community the plots in the database belong to. Got {0} for current community in settings file and {1} for community plots belong to'.format(settings.CURRENT_COMMUNITY, getattr(items[0], mapper_class.map_area_field_attr)))
        return self.get_registry(settings.CURRENT_COMMUNITY)

    def get_mapper_as_tuple(self):
        """Returns a list of tuples from the registry dictionary in the format of choices used by models."""
        return [(l, l) for l in self.get_as_list()]

    def register(self, mapper_cls):
        """Registers a given mapper class to the site registry."""
        self.set_registry(mapper_cls)

    def autodiscover(self):
        """Autodiscovers mapper classes in the mapper.py file of any INSTALLED_APP."""
        if not self.autodiscovered:
            for app in settings.INSTALLED_APPS:
                mod = import_module(app)
                try:
                    before_import_registry = copy.copy(site_mappers._registry)
                    import_module('%s.mappers' % app)
                except:
                    site_mappers._registry = before_import_registry
                    if module_has_submodule(mod, 'mappers'):
                        raise
            self.autodiscovered = True
            if not self.get_registry(settings.CURRENT_MAPPER):
                raise ImproperlyConfigured('Settings attribute CURRENT_MAPPER does not refer to a valid mapper. Got {0}'.format(settings.CURRENT_MAPPER))
site_mappers = Controller()
