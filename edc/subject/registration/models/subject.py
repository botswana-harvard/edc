import re

from uuid import uuid4

from django.db import models, transaction

from edc.core.identifier.exceptions import IdentifierError
from django.core.exceptions import MultipleObjectsReturned


class Subject(models.Model):
    """Base for registered subject models."""

    def save(self, *args, **kwargs):
        using = kwargs.get('using')
        self.set_uuid_as_subject_identifier_if_none()
        self.raise_on_duplicate_subject_identifier(using)
        self.raise_on_changed_subject_identifier(using)
        super(Subject, self).save(*args, **kwargs)

    def raise_on_changed_subject_identifier(self, using):
        if self.id:
            with transaction.atomic():
                obj = self.__class__.objects.get(pk=self.id)
                if obj.subject_identifier != self.subject_identifier_as_pk:
                    if self.subject_identifier != obj.subject_identifier:
                        raise IdentifierError(
                            'Subject identifier cannot be changed for existing registered subject. '
                            'Got {}.'.format(self.subject_identifier))

    def raise_on_duplicate_subject_identifier(self, using):
        """Checks if the subject identifier is in use, for new and existing instances."""
        with transaction.atomic():
            error_msg = (
                'Attempt to insert or update duplicate value for subject_identifier {0} '
                'when saving {1} '.format(self.subject_identifier, self))
            try:
                obj = self.__class__.objects.using(using).get(
                    subject_identifier=self.subject_identifier)
                if obj.id != self.id:
                    raise IdentifierError(error_msg)
            except self.__class__.DoesNotExist:
                pass
            except MultipleObjectsReturned:
                raise IdentifierError(error_msg)

    def set_uuid_as_subject_identifier_if_none(self):
        """Inserts a random uuid as a dummy identifier for a new instance.

        Model uses subject_identifier_as_pk as a natural key for
        serialization/deserialization. Value must not change once set."""
        if not self.subject_identifier_as_pk:
            self.subject_identifier_as_pk = str(uuid4())  # this will never change
            if not self.subject_identifier:
                self.subject_identifier = self.subject_identifier_as_pk

    def get_subject_identifier(self):
        return self.subject_identifier

    def include_for_dispatch(self):
        return True

    class Meta:
        abstract = True
