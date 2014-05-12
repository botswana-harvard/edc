import copy
import re
import inspect

from django.conf import settings
from django.conf.urls import patterns, url
from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.utils import translation

from edc.base.model.models import BaseModel
from edc.core.bhp_common.utils import convert_from_camel
from edc.core.bhp_context.classes import BaseContext
from edc.dashboard.section.classes import site_sections
from edc.subject.registration.models import RegisteredSubject


class Dashboard(object):

#     context = BaseContext()
    dashboard_name = None  # e.g. 'Dashboard'
    dashboard_url_name = None   # e.g. 'dashboard_url_name'
    template = None

    def __init__(self, dashboard_type, dashboard_id, dashboard_model, dashboard_type_list=None, dashboard_models=None):

        self.dashboard_type_list = dashboard_type_list
        self.dashboard_models = dashboard_models
        self.dashboard_type = dashboard_type
        self.dashboard_model = dashboard_model
        self.dashboard_model_name = dashboard_model
        self.dashboard_id = dashboard_id
        self.context = BaseContext()
#         self.search_type = self.section.get_search_type(self.get_section_name())
        # TODO: what about section, section name methods?

    @classmethod
    def add_to_urlpattern_string(cls):
        """Returns a fragment of a url regular expression to be added to the urlpattern string in :func:`get_urlpatterns`."""
        return ''

    @classmethod
    def add_to_urlpattern_string_kwargs(cls):
        """Returns a dictionary to compliment the url regular expression fragment returned by :func:`add_to_urlpattern_string`."""
        return {}

    def add_to_context(self):
        pass

    def _add_to_context(self):
        self.context.add(template=self.template,
            dashboard_type=self.dashboard_type,
            dashboard_id=self.dashboard_id,
            dashboard_model=self.dashboard_model_name,  # yes, we use the name not the model class for the context
            dashboard_model_instance=self.dashboard_model_instance,
            dashboard_name=self.dashboard_name,
            dashboard_url_name=self.dashboard_url_name,
            home_url=self.home_url)
        self.add_to_context()

    @property
    def home_url(self):
        """Returns a home url."""
        return reverse(
            self.dashboard_url_name,
            kwargs={
                'dashboard_type': self.dashboard_type,
                'dashboard_model': self.dashboard_model_name,
                'dashboard_id': self.dashboard_id}
            )

    @property
    def dashboard_type(self):
        return self._dashboard_type

    @dashboard_type.setter
    def dashboard_type(self, value=None):
        """Sets the dashboard type to a value that must be listed in dashboard_type_list."""
        self._dashboard_type = value
        if not self._dashboard_type in self.dashboard_type_list:
            raise TypeError('Invalid dashboard type. Expected one of {0}'.format(self.dashboard_type_list))

    @property
    def dashboard_model(self):
        return self._dashboard_model

    @dashboard_model.setter
    def dashboard_model(self, model_or_model_name):
        """Sets the model class given by the dashboard URL.

        Checks with attribute \'dashboard_models \' if model or model_name is known to the class before using it."""
        self._dashboard_model = self.dashboard_models.get(model_or_model_name)
        if not self._dashboard_model:
            if convert_from_camel(model_or_model_name._meta.object_name) in self.dashboard_models:
                self._dashboard_model = model_or_model_name

    @property
    def dashboard_model_name(self):
        return self._dashboard_model_name

    @dashboard_model_name.setter
    def dashboard_model_name(self, model_or_model_name):
        """Sets to a model name either explicitly or from a Model class."""
        try:
            self._dashboard_model_name = convert_from_camel(model_or_model_name._meta.object_name)
        except AttributeError:
            self._dashboard_model_name = model_or_model_name

    @property
    def dashboard_id(self):
        return self._dashboard_id

    @dashboard_id.setter
    def dashboard_id(self, value=None):
        """Sets the pk of the dashboard model class given by the dashboard URL."""
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if not re_pk.match(value or ''):
            raise TypeError('Dashboard id must be a uuid (pk). Got {0}'.format(value))
        self._dashboard_id = value

    def get_context_prep(self, **kwargs):
        pass

    def get_create_prep(self, **kwargs):
        pass

    def set_context(self):
        self._add_to_context()

    @property
    def search_type(self):
        return self.section.get_search_type(self.get_section_name())

    @property
    def section(self):
        return self._section

    @section.setter
    def section(self, section_name):
        """Sets the instance of the section class for the dashboard."""
        section = site_sections.get(section_name)
        if not section:
            if site_sections.get_section_names() == []:
                raise TypeError('class site_sections is not set up. Call autodoscover first.')
            section = site_sections.get(section_name)
        if not section:
            raise TypeError('Could not find section \'{0}\' in site_sections. You need to define a section class for this name in section.py.'.format(section_name))
        self._section = section()

    @property
    def section_name(self):
        return self.section.get_section_name()

    @property
    def dashboard_model_instance(self):
        return self.dashboard_model.objects.get(pk=self.dashboard_id)

    def verify_dashboard_model(self, value):
        """Verifies the dashboard model(s) in dictionary \'value\' before adding to the dictionary and throws an exception if unable to verify.

        Users may override to test the model for methods or subclass, etc."""
        pass

    def add_dashboard_model(self, value):
        """Adds additional items to the dashboard models dictionary.

        This dictionary is used to verify the dashboard_model name or class
        coming from the url. We only want ones that we expect."""
        if not value:
            raise TypeError('parameter \'value\' may not be None. Expected a model class or function.')
        if not isinstance(value, dict):
            raise TypeError('Parameter \'value\' must be a dictionary.')
        for name, model_or_func in value.iteritems():
            if (inspect.ismethod(model_or_func) or inspect.isfunction(model_or_func)) and model_or_func.__name__ in ['_get_visit_model', 'get_visit_model']:
                value[name] = value[name]()  # may be a function (that returns a model) TODO: may we allow more than just get_visit_model?
                if not issubclass(value[name], BaseModel):
                    raise TypeError('Expected a subclass of BaseModel from function \'get_visit_model\'. Got {0}.'.format(value))
            elif issubclass(model_or_func, BaseModel):
                pass  # may be a model
            elif isinstance(model_or_func, tuple):
                value[name] = models.get_model(model_or_func[0], model_or_func[1])
            else:
                raise TypeError('Dictionary of {{k, v}} must have value attribute v of base class BaseModel or a method that returns a model class. Got {0} for {1}'.format(type(model_or_func), value))
        self.verify_dashboard_model(value)
        self._dashboard_models.update(value)

    @property
    def dashboard_models(self):
        return copy.deepcopy(self._dashboard_models)

    @dashboard_models.setter
    def dashboard_models(self, value):
        """Sets a reference dictionary by updating the user defined dictionary with a default for registered_subject."""
        self._dashboard_models = {'registered_subject': RegisteredSubject}
        if value:
            self.add_dashboard_model(value)

    @property
    def extra_url_context(self):
        return self._extra_url_context

    @extra_url_context.setter
    def extra_url_context(self, value):
        self._extra_url_context = value
        default_value = '&form_language_code={0}'.format(self.language)
        if default_value not in self._extra_url_context:
            self._extra_url_context = '{0}{1}'.format(self._extra_url_context, '&form_language_code={0}'.format(self.language))

    @property
    def language(self):
        """Returns the language of consent.

        If the consent has not been defined for this dashboard, just take the settings LANGUAGE attribute."""
        if self.consent:
            self.consent.language
            translation.activate(self.consent.language)
            self._language = translation.get_language()
        else:
            self._language = settings.LANGUAGE_CODE
        return self._language

    @classmethod
    def get_urlpatterns(self, pattern_prefix, urlpattern_string_kwargs, view=None, **kwargs):
        """Gets the url_patterns for the dashboard view.

        Called in the urls.py of the local xxxx_dashboard app. For example::

            from django.contrib import admin
            from django.conf.urls import patterns, url
            from dom_dashboard.classes import InfantDashboard, MaternalDashboard

            urlpattern_string_kwargs = {}
            urlpattern_string_kwargs['dashboard_type'] = 'infant'
            urlpattern_string_kwargs['dashboard_model'] = 'infant_birth'
            urlpatterns = InfantDashboard.get_urlpatterns('dom_dashboard.views', urlpattern_string_kwargs, visit_field_names=['infant_visit', ])

            urlpattern_string_kwargs = {}
            urlpattern_string_kwargs['dashboard_type'] = 'maternal'
            urlpattern_string_kwargs['d-ashboard_model'] = 'maternal_consent'
            urlpatterns += MaternalDashboard.get_urlpatterns('dom_dashboard.views', urlpattern_string_kwargs, visit_field_names=['maternal_visit', ])
        """

        # FIXME: this is confusing!!!!!

        if not self.dashboard_url_name:
            raise ImproperlyConfigured('class attribute \'dashboard_url_name\' may not be None')
        if not pattern_prefix:
            raise ImproperlyConfigured('Parameter \'pattern_prefix\' may not be None. Must be app_label.view_module, (e.g. maikalelo_dashboard.views). See your urls.py.')
        view = view or self.view
        if not view:
            raise ImproperlyConfigured('Parameter \'view\' may not be None. Must be a valid view name, such as \'infant_dashboard\'.')
        if not urlpattern_string_kwargs:
            raise ImproperlyConfigured('Parameter \'urlpattern_string_kwargs\' may not be None.')
        if not isinstance(urlpattern_string_kwargs, dict):
            raise ImproperlyConfigured('Parameter \'urlpattern_string_kwargs\' must be a dictionary. Got {0}'.format(urlpattern_string_kwargs))
        # add default re patterns
        urlpattern_string_kwargs['pk'] = '[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}'

        # FIXME: need to move to registeredSubjectDashboard as these regexs are
        # specific to it, '|visit|appointment|registered_subject'
        # should use the add_to_urlpattern_string_kwargs()
        # and probably do not need to set these in urls!
        if urlpattern_string_kwargs.get('dashboard_model', None):
            urlpattern_string_kwargs['dashboard_model'] += '|visit|appointment|registered_subject'
        else:
            urlpattern_string_kwargs.update({'dashboard_model': 'visit|appointment|registered_subject'})
        if not urlpattern_string_kwargs.get('dashboard_type', None):
            urlpattern_string_kwargs.update({'dashboard_type': 'subject'})

        # add user patterns
        urlpattern_string_kwargs.update(self.add_to_urlpattern_string_kwargs())
        # add extra key/value to the pattern string, if the user has overriden the method add_to_urlpattern_string
        urlpattern_string = r'^(?P<dashboard_type>{{dashboard_type}})/(?P<dashboard_model>{{dashboard_model}})/(?P<dashboard_id>{{pk}})/{0}$'.format(self.add_to_urlpattern_string())
        urlpatterns = patterns(pattern_prefix,
            url(urlpattern_string.format(**urlpattern_string_kwargs),
                view,
                name=self.dashboard_url_name
                ))
        return urlpatterns
