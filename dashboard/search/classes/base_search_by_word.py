from django.db import models
from django.db.models import Q

from edc.core.crypto_fields.fields import BaseEncryptedField
from edc.subject.registration.models import RegisteredSubject
from edc.subject.consent.models import BaseConsent

from ..exceptions import SearchError

from .base_searcher import BaseSearcher


class BaseSearchByWord(BaseSearcher):

    def __init__(self):
        super(BaseSearchByWord, self).__init__()
        self.search_helptext = 'Search by search term.'
        self.search_result_order_by = '-modified'

    def contribute_to_context(self, context):
        context = super(BaseSearchByWord, self).contribute_to_context(context)
        context.update({
            'search_filter_keywords': self.get_filter_keyword_list()})
        return context

    def get_search_result(self, request, **kwargs):
        """Returns a queryset using the search term as a filter."""
        model = self.get_search_model_cls()
        search_form = self.get_search_form(self.get_search_form_data())
        if search_form.is_valid():
            qset_filter = Q()
            qset_exclude = Q()
            self.set_search_term(search_form.cleaned_data.get('search_term'))
            if self.get_qset_by_filter_keyword():
                qset_filter, qset_exclude = self.get_qset_by_filter_keyword()
            elif self.get_qset_by_search_term_pattern():
                qset_filter, qset_exclude = self.get_qset_by_search_term_pattern()
            elif 'registered_subject' in dir(model()):
                qset_filter = self.get_qset_for_registered_subject()
            elif issubclass(model, BaseConsent):
                qset_filter = self.get_qset_for_consent()
            else:
                qset_filter = self.get_qset_for_generic_model()
            search_result = model.objects.filter(qset_filter).exclude(qset_exclude).order_by('-modified', '-created')
        return search_result

    def get_filter_keyword_list(self):
        return []

    def get_filter_keyword_url_list(self):
        return []

    def get_qset_by_filter_keyword(self):
        """Returns a qset based on matching keyword.

        If you predefine keywords, the search term will be intercepted and used to select a query instead."""
        return None

    def get_qset_by_search_term_pattern(self):
        """Returns a qset based on a matching pattern.

        If you predefine a pattern, the search term will be intercepted and applied to a custom query."""
        return None

    def get_qset_for_registered_subject(self):
        search_term_or_hash = self.hash_for_encrypted_fields(self.get_search_term(), RegisteredSubject())
        self.set_order_by('registered_subject__subject_identifier')
        qset = (
            Q(registered_subject__subject_identifier__icontains=search_term_or_hash.get('subject_identifier')) |
            Q(registered_subject__first_name__exact=search_term_or_hash.get('first_name')) |
            Q(registered_subject__initials__icontains=search_term_or_hash.get('initials')) |
            Q(registered_subject__sid__icontains=search_term_or_hash.get('sid')) |
            Q(registered_subject__last_name__exact=search_term_or_hash.get('last_name')) |
            Q(registered_subject__identity__exact=search_term_or_hash.get('identity')) |
            Q(user_created__icontains=search_term_or_hash.get('user_created')) |
            Q(user_modified__icontains=search_term_or_hash.get('user_modified'))
            )
        return qset

    def get_qset_for_consent(self):
        search_term_or_hash = self.hash_for_encrypted_fields(self.get_search_term(), self.get_search_model_cls())
        self.set_order_by('subject_identifier')
        qset = (
            Q(subject_identifier__icontains=search_term_or_hash.get('subject_identifier')) |
            Q(first_name__exact=search_term_or_hash.get('first_name')) |
            Q(last_name__exact=search_term_or_hash.get('last_name')) |
            Q(identity__exact=search_term_or_hash.get('identity')) |
            Q(initials__contains=search_term_or_hash.get('initials')) |
            Q(user_created__icontains=search_term_or_hash.get('user_created')) |
            Q(user_modified__icontains=search_term_or_hash.get('user_modified'))
            )
        return qset

    def get_qset_for_generic_model(self):
        qset = Q()
        search_term_or_hash = self.hash_for_encrypted_fields(self.get_search_term(), self.get_search_model_cls())
        self.set_order_by('-modified')
        for field in self.get_search_model_cls()._meta.fields:
            if isinstance(field, BaseEncryptedField):
                qset.add(Q(**{'{0}__exact'.format(field.name): search_term_or_hash.get(field.name)}), Q.OR)
            elif isinstance(field, (models.CharField, models.TextField)):
                qset.add(Q(**{'{0}__icontains'.format(field.name): search_term_or_hash.get(field.name)}), Q.OR)
            elif isinstance(field, (models.IntegerField, models.FloatField, models.DecimalField)):
                try:
                    int(self.get_search_term())
                    qset.add(Q(**{'{0}__exact'.format(field.name): search_term_or_hash.get(field.name)}), Q.OR)
                except:
                    pass
            elif isinstance(field, (models.DateTimeField, models.DateField)):
                pass
            elif isinstance(field, (models.ForeignKey, models.OneToOneField, models.ManyToManyField, models.ImageField)):
                pass
            else:
                raise SearchError('model contains a field type not handled. Got {0} from model {1}.'.format(field, self.get_search_model_cls()))
        return qset
