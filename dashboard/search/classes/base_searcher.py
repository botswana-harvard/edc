from django.core.exceptions import ImproperlyConfigured
from django.conf.urls import patterns, url
from django.db.models import get_model
from django import forms
from edc.core.crypto_fields.fields import BaseEncryptedField
from ..forms import SearchForm
from ..exceptions import SearchModelError


class BaseSearcher(object):

    """ Base search class. """

    APP_LABEL = 0
    MODEL_NAME = 1
    search_model = None
    search_form = None
    template = None
    search_model_attrname = None

    def __init__(self):
        self._name = None
        self._search_term = None
        self._search_model_cls = None
        self._search_form_data = None
        self._context = {}
        self._order_by = None
        self._search_result_template = None
        self.form_is_valid = False
        self.registration_model = {}
        self._search_form = None
        self.search_label = None
        self.search_model_name = None
        self.set_name()
        self.set_search_form()

    def contribute_to_context(self, context):
        context.update({'search_form': self.get_search_form(self.get_search_form_data())})
        return context

    def _get_search_result(self, request, **kwargs):
        return self.get_search_result(request, **kwargs)

    def get_search_result(self, request, **kwargs):
        """ Returns a queryset or other iterable of search result.

        Users must override this to define custom search logic. """
        raise ImproperlyConfigured('Method get_search_result must be overridden to return a search result based on criteria from the request object.')
        return None

    def set_name(self):
        self._name = self.name
        if not self._name:
            raise AttributeError('Attribute name may not be None for {0}.'.format(self))

    def get_name(self):
        return self._name

    def set_search_form(self):
        self._search_form = self.search_form or SearchForm
        if not issubclass(self._search_form, forms.Form):
            raise AttributeError('Expected subclass of forms.Form for attribute \'search_form\'. Got {0}'.format(self._search_form))

    def get_search_form(self, data=None):
        return self._search_form(data)

    def set_search_form_data(self, form_data=None):
        self._search_form_data = {}
        if self.get_search_form(form_data).is_valid():
            self._search_form_data = form_data

    def get_search_form_data(self):
        return self._search_form_data

    def set_search_term(self, value):
        if not value:
            raise TypeError('Search term may not be None')
        self._search_term = str(value).strip()

    def get_search_term(self):
        return self._search_term

    def set_order_by(self, *args):
        self._order_by = args

    def get_order_by(self):
        return self._order_by

    def set_search_result_include_template(self, template=None):
        if template:
            self._search_result_template = template
        elif self.template:  # try for class attribute first
            self._search_result_template = self.template
        else:
            self._search_result_template = '{0}_include.html'.format(self.get_search_model_cls()._meta.object_name.lower())

    def get_search_result_include_template(self):
        if not self._search_result_template:
            self.set_search_result_include_template()
        return self._search_result_template

    def _set_search_model_cls(self, value=None):
        if self.search_model:
            if isinstance(self.search_model, tuple):
                self._search_model_cls = get_model(self.search_model[0], self.search_model[1])
            else:
                self._search_model_cls = self.search_model
        if not self._search_model_cls:
            raise SearchModelError('Attribute \'search_model_cls\' cannot be None')

    def get_search_model_cls(self):
        if not self._search_model_cls:
            self._set_search_model_cls()
        return self._search_model_cls

    def get_url_patterns(self, view, section_name=None):
        """Returns a url pattern which includes the section prefix of the url pattern.

        This is called by the section class."""
        # TODO: can section be removed from this??
        if section_name:
            return patterns('',
            url(r'^(?P<section_name>{section_name})/(?P<search_name>{search_name})/(?P<search_term>[\d\w\ \-\<\>]+)/$'.format(section_name=section_name, search_name=self.get_name()),
                view,
                name="section_search_{name}_url".format(name=self.get_name())),
            url(r'^(?P<section_name>{section_name})/(?P<search_name>{search_name})/$'.format(section_name=section_name, search_name=self.get_name()),
                view,
                name="section_search_{name}_url".format(name=self.get_name())))
        return patterns('',
        url(r'^(?P<search_name>{search_name})/(?P<search_term>{search_term})/$'.format(search_name=self.get_name(), search_term=self.get_search_term()),
            view,
            name="search_{name}_url".format(name=self.get_name())),
        url(r'^(?P<search_name>{search_name})/$'.format(search_name=self.get_name()),
            view,
            name="search_{name}_url".format(name=self.get_name())))

    def hash_for_encrypted_fields(self, search_term, model_instance):
        """ Using the model's field objects and the search term, create a dictionary of
        {field_name, search term} where search term is hashed if this is an encrypted field """
        terms = {}
        for field in model_instance._meta.fields:
            if isinstance(field, BaseEncryptedField):
                # change the search term to a hash using the hasher on the field
                terms[field.attname] = field.field_cryptor.get_hash_with_prefix(search_term)
            else:
                # use the original search term
                terms[field.attname] = search_term
        return terms
