from django.db import models
from edc.base.model.models import BaseUuidModel
from edc.subject.registration.models import RegisteredSubject
from ..choices import ENTRY_STATUS


class BaseEntryBucket(BaseUuidModel):

    """ Base model for list of required entries by registered_subject. """

    registered_subject = models.ForeignKey(RegisteredSubject, related_name='+')
    current_entry_title = models.CharField(
        max_length=250,
        null=True)
    entry_status = models.CharField(
        max_length=25,
        choices=ENTRY_STATUS,
        default='NEW',
        db_index=True)
    due_datetime = models.DateTimeField(
        null=True,
        blank=True)
    report_datetime = models.DateTimeField(
        null=True,
        blank=True)
    entry_comment = models.TextField(
        max_length=250,
        null=True,
        blank=True)
    close_datetime = models.DateTimeField(
        null=True,
        blank=True)
    fill_datetime = models.DateTimeField(
        null=True,
        blank=True)

    def include_for_dispatch(self):
        return True

    class Meta:
        abstract = True
