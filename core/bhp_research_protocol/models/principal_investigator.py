from django.utils.translation import ugettext as _
from edc.base.model.models import BaseUuidModel
from edc.base.model.fields import NameField, InitialsField


class PrincipalInvestigator (BaseUuidModel):

    first_name = NameField(
        verbose_name=_("First name")
        )

    last_name = NameField(
        verbose_name=_("Last name")
    )

    initials = InitialsField()

    def __unicode__(self):
        return '%s, %s' % (self.last_name, self.first_name)

    class Meta:
        ordering = ['last_name', 'first_name']
        unique_together = ['last_name', 'first_name']
        app_label = 'bhp_research_protocol'
