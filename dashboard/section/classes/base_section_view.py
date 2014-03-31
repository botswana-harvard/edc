from django.conf import settings
from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.template import RequestContext

from .most_recent_query import MostRecentQuery


class BaseSectionView(object):

    section_name = None
    section_display_name = None
    section_display_index = None
    section_template = None
    add_model = None
    search = None
    default_search = None

    def __init__(self):
        self._context = {}
        self._template = None
        self._section_name = None
        self._section_display_name = None
        self._section_display_index = None
        self._add_model_cls = None
        self._section_list = None
        self.set_section_name()
        self.set_section_display_name()
        self.set_section_display_index()
        self.set_template()
        self.set_add_model_cls()
        # search stuff
        self._searchers = None
        self._searcher = None
        self._default_searcher = None
        self.set_searchers()
        self.set_default_searcher()

    @property
    def context(self):
        """Returns the template context."""
        return self._context

    def update_context(self, **kwargs):
        """Updates the template context."""
        for k, v in kwargs.iteritems():
            self._context[k] = v

    @property
    def protocol_lab_section(self):
        if 'LAB_SECTION' in dir(settings):
            return settings.LAB_SECTION
        else:
            return ''

    def set_section_name(self):
        """Sets the name for this section."""
        self._section_name = self.section_name
        if not self._section_name:
            raise AttributeError('Attribute section name cannot be None.')

    def get_section_name(self):
        """Returns the name for this section."""
        if not self._section_name:
            self.set_section_name()
        return self._section_name

    def set_section_display_name(self):
        """Sets the name for this section."""
        if self.section_display_name:
            self._section_display_name = self.section_display_name

    def get_section_display_name(self):
        """Returns the name for this section."""
        return self._section_display_name

    def set_section_display_index(self):
        self._section_display_index = self.section_display_index
        if not self._section_display_index:
            raise AttributeError('Attribute section_display_index cannot be None')

    def get_section_display_index(self):
        """Returns the index for this section used to order the navigation buttons."""
        return self._section_display_index

    def set_add_model_cls(self):
        self._add_model_cls = self.add_model

    def get_add_model_cls(self):
        """Returns the model class used for the 'Add' button."""
        return self._add_model_cls

    def get_add_model_name(self):
        """Returns the verbose name of the model class for the 'Add' button."""
        if self.get_add_model_cls():
            return self.get_add_model_cls()._meta.verbose_name
        return None

    def get_add_model_opts(self):
        """Returns the _meta options of the model class for the 'Add' button."""
        if self.get_add_model_cls():
            return self.get_add_model_cls()._meta
        return None

    def set_template(self, template=None):
        """Sets the template for this section."""
        if self.section_template:
            self._template = self.section_template
        else:
            self._template = self.get_default_template()

    def get_template(self):
        return self._template

    def get_default_template(self):
        """Returns a default template is none set."""
        return 'section_{0}.html'.format(self.get_section_name())

    def set_section_list(self, value):
        """Sets a list of section names. Called in urls.py through the controller."""
        #print value
        self._section_list = value

    def get_section_list(self):
        """Returns the section list."""
        return self._section_list

    def _get_section_url_patterns(self, view):
        return patterns('',
            url(r'^(?P<section_name>{section_name})/$'.format(section_name=self.get_section_name()),
                view,
                name="section_url"))

    def urlpatterns(self, view=None):
        """ Generates urlpatterns for the view of this section.

        If search classes have been added to this section class, search urls will be added before the section urls.
        """
        if view is None:
            view = self._view
        url_patterns = []
        url_patterns += self.get_search_url_patterns(view)
        url_patterns += self._get_section_url_patterns(view)
        return url_patterns

    def _contribute_to_context_wrapper(self, context, request, *args, **kwargs):
        """Wraps :func:`contribute_to_context`."""
        context = self.contribute_to_context(context, request, *args, **kwargs)
        return context

    def contribute_to_context(self, context, request, *args, **kwargs):
        """Users may override to update the template context with {key, value} pairs."""
        return context

    def _paginate(self, search_result, page=1, results_per_page=None):
        """Paginates the search result queryset after which templates
        access search_result.object_list.

        Also sets the 'magic_url' for previous/next paging urls

        Keyword Arguments:
            results_per_page: (default: 25)
        """
        if not results_per_page:
            results_per_page = 25
        if search_result:
            paginator = Paginator(search_result, results_per_page)
            try:
                search_result = paginator.page(page)
            except (EmptyPage, InvalidPage):
                search_result = paginator.page(paginator.num_pages)
        return search_result

    def view(self, request, *args, **kwargs):
        """Default view for this section called by :func:`_view`.

        .. note:: Instead of overriding, try adding to the context using :func:`contribute_to_context`.

        Default context includes::
            * app_name: settings.APP_NAME,
            * installed_apps: settings.INSTALLED_APPS,
            * selected_section: from :func:`get_section_name`,
            * sections: from :func:`get_section_list`,
            * section_name: from :func:`get_section_name`,
            * add_model: from :func:`get_add_model_cls`,
            * add_model_opts: from :func:`get_add_model_opts`,
            * add_model_name: from :func:`get_add_model_name`,
        """
#         search_term = request.GET.get('search_term', '')  # might be passed by the querystring
        page = request.GET.get('page')
        default_context = {}
        search_result = None
        for searcher in self.get_searchers().itervalues():
            # if searchers, get any context, such as the search forms, for the template
            searcher.contribute_to_context(default_context)
        # try to select a searcher with the POST data or URL data
        self.set_searcher(kwargs.get('search_name'), [request.POST, kwargs])
        if self.get_searcher():
                page = 1
                search_result = self.get_searcher().get_search_result(request, **kwargs)
                default_context.update({
                    'search_result': self._paginate(search_result, page),
                    'search_result_include_file': self.get_searcher().get_search_result_include_template(),
                    })
        else:
            if self.get_default_searcher():
                default_context.update({
                    'search_result': self._paginate(MostRecentQuery(self.get_default_searcher().get_search_model_cls()).query(), page),
                    'search_result_include_file': self.get_default_searcher().get_search_result_include_template(),
                    })
        default_context.update({
            'app_name': settings.APP_NAME,
            'installed_apps': settings.INSTALLED_APPS,
            'selected_section': self.get_section_name(),
            'sections': self.get_section_list(),
            'sections_names': [sec[0] for sec in self.get_section_list()],
            'section_name': self.get_section_name(),
#             'search_term': search_term,
            'add_model': self.get_add_model_cls(),
            'add_model_opts': self.get_add_model_opts(),
            'add_model_name': self.get_add_model_name(),
            'protocol_lab_section': self.protocol_lab_section,
            })
        # add extra values to the context dictionary
        context = self._contribute_to_context_wrapper(default_context, request, **kwargs)
        return render_to_response(self.get_template(), context, context_instance=RequestContext(request))

    def _view(self, request, *args, **kwargs):
        """Wraps :func:`view` method to force login and treat this like a class based view."""
        @login_required
        def view(request, *args, **kwargs):
            return self.view(request, *args, **kwargs)
        return view(request, *args, **kwargs)

    def set_searchers(self):
        """Sets the dictionary of search class instances.

        Format is {search_name: search_instance} where search_name is the name attribute on the search class.
        The name is returned to this class by the search url. See also method urlpatterns"""
        self._searchers = {}
        if isinstance(self.search, list):
            for search_cls in self.search:
                self._searchers.update({search_cls.name: search_cls()})
        elif isinstance(self.search, dict):
            for search_cls in self.search.itervalues():
                self._searchers.update({search_cls.name: search_cls()})
        else:
            pass

    def get_searchers(self):
        """Returns a dictionary of searchers by name."""
        return self._searchers

    def set_searcher(self, name, data_list):
        """Sets the searcher to the one that has a form that will validate with data in the data list.

        The data list is either a POST dictionary or kwargs dictionary populated by the url"""
        self._searcher = None
        if name:
            if not self.get_searchers().get(name):
                raise AttributeError('Cannot find search class for name \'{0}\' in dictionary {1}.'.format(name, self.get_searchers()))
            for data in data_list:
                if self.get_searchers().get(name).get_search_form(data).is_valid():
                    self.get_searchers().get(name).set_search_form_data(data)
                    self._searcher = self.get_searchers().get(name)
                    break

    def get_searcher(self):
        """Returns the current searcher."""
        return self._searcher

    def set_default_searcher(self):
        """Sets one search class as the default."""
        if self.default_search:
            self._default_searcher = self.default_search()
        else:
            if len(self.get_searchers().items()) >= 1:
                self._default_searcher = self.get_searchers().values()[0]

    def get_default_searcher(self):
        return self._default_searcher

    def get_search_url_patterns(self, view):
        url_patterns = []
        for search_inst in self.get_searchers().itervalues():
            url_patterns += search_inst.get_url_patterns(view, self.get_section_name())
        return url_patterns
