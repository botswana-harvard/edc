import copy

from collections import OrderedDict

from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.importlib import import_module
from django.utils.module_loading import module_has_submodule

from edc.device.device.classes import device

from ..exceptions import MapperError

from .mapper import Mapper


class AlreadyRegistered(Exception):
    pass


class NotRegistered(Exception):
    pass


class Controller(object):

    """ Main controller of :class:`Mapping` objects. """

    def __init__(self):
        self._registry = OrderedDict()
        self._registry_by_code = OrderedDict()
        self.autodiscovered = False

    def __iter__(self):
        return self._registry.itervalues()

    def sort_by_code(self):
        """Sorts the registries by map_code."""
        codes = []
        mappers = OrderedDict()
        mappers_by_code = OrderedDict()
        for mapper in self._registry_by_code.itervalues():
            codes.append(mapper.map_code)
        codes.sort()
        for code in codes:
            mappers.update({self._registry_by_code.get(code).map_area: self._registry_by_code.get(code)})
            mappers_by_code.update({self._registry_by_code.get(code).map_code: self._registry_by_code.get(code)})
        self._registry = mappers
        self._registry_by_code = mappers_by_code

    def set_registry(self, mapper_cls):
        """Registers a given mapper class to the site registry."""
        if not issubclass(mapper_cls, Mapper):
            raise MapperError('Expected a subclass of Mapper.')
        # use map_area class attribute add the dictionary key
        if mapper_cls.map_area in self._registry:
            raise AlreadyRegistered('The mapper class {0} is already registered ({1})'.format(mapper_cls, mapper_cls.map_area))
        self._registry[mapper_cls.map_area] = mapper_cls
        self._registry_by_code[mapper_cls.map_code] = mapper_cls

    def get(self, name):
        """Returns a key, value pair from the dictionary for the given key."""
        return self._registry.get(name)

    def get_by_code(self, code):
        """Returns a key, value pair from the dictionary for the given key."""
        return self._registry_by_code.get(code)

    def get_registry(self, name=None):
        """Returns the site mapper registry dictionary."""
        if name:
            if name in self.registry:
                return self.registry.get(name)
            else:
                raise MapperError('{0} is not a valid mapper name in {1}.'.format(name, self.registry))
        return self.registry

    @property
    def registry(self):
        """Returns the site mapper registry dictionary.

        Use this instead of get_registry()"""
        return self._registry

    def get_as_list(self):
        """Returns a list of dictionary keys from the registry dictionary to be used as a list of map areas or communities."""
        lst = [k for k in self._registry]
        lst.sort()
        return lst

    def get_current_mapper(self):
        """Returns the mapper class for the current community."""
        return self.registry.get(self.valid_community_configuration)

    @property
    def current_mapper(self):
        """Returns the mapper class for the current community."""
        return self.registry.get(self.valid_community_configuration)

    @property
    def valid_community_configuration(self):
        """Returns the current community after some validation.

        Uses the settings attribute CURRENT_COMMUNITY as the key.

        If CURRENT_COMMUNITY_CHECK is set to True or is not set,
        the value of CURRENT_COMMUNITY will be checked against
        plot information before returning the mapper."""
        try:
            current_community = settings.CURRENT_COMMUNITY
        except AttributeError:
            raise MapperError('Missing settings attribute CURRENT_COMMUNITY. '
                              'Please update settings.py. e.g. CURRENT_COMMUNITY = \'otse\'.')
        try:
            community_check = settings.CURRENT_COMMUNITY_CHECK
        except AttributeError:
            community_check = True
        if community_check:
            if not device.is_server:
                mapper_class = self.registry.get(current_community)
                correct_identifiers = mapper_class.item_model.objects.filter(
                    plot_identifier__startswith=mapper_class.map_code).count()
                all_identifiers = mapper_class.item_model.objects.all().count()
                if correct_identifiers != all_identifiers:
                    raise MapperError('Settings attribute CURRENT_COMMUNITY does not match the plot identifiers. '
                                      'Got {0}/{1} plot identifiers starting with {2}'.format(
                                          correct_identifiers,
                                          all_identifiers,
                                          current_community,)
                                      )
        return current_community

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
            if not self.registry.get(settings.CURRENT_MAPPER):
                raise ImproperlyConfigured('Settings attribute CURRENT_MAPPER does not refer to a valid mapper. Got {0}'.format(settings.CURRENT_MAPPER))
site_mappers = Controller()
