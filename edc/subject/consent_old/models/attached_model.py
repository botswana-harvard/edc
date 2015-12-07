from django.db import models
from edc_base.audit_trail import AuditTrail
from edc_base.model.models import BaseUuidModel
from edc.core.bhp_content_type_map.models import ContentTypeMap
from ..managers import AttachedModelManager
from .consent_catalogue import ConsentCatalogue


class AttachedModel(BaseUuidModel):
    """Models that are linked to a catalogue entry.

    Search the attached models by content_type_map to determine the consent_catalogue and from that, the consent model."""
    consent_catalogue = models.ForeignKey(ConsentCatalogue)

    # the content type map of a subject model
    content_type_map = models.ForeignKey(ContentTypeMap,
        verbose_name='Subject model')

    is_active = models.BooleanField(default=True)

    history = AuditTrail()

    objects = AttachedModelManager()

    def natural_key(self):
        return self.consent_catalogue.natural_key() + self.content_type_map.natural_key()

    def __unicode__(self):
        return self.content_type_map.model

    class Meta:
        app_label = 'consent'
        db_table = 'bhp_consent_attachedmodel'  # TODO: refactor SQL schema to remove
        unique_together = (('consent_catalogue', 'content_type_map'), )
