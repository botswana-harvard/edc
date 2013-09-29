from django.db import models
from funding_source import FundingSource


class Protocol(models.Model):

    protocol_identifier = models.CharField(
        max_length=25,
        null=True,
        )

    research_title = models.TextField(max_length=250)

    short_title = models.CharField(max_length=25)

    site_name_fragment = models.CharField(max_length=25,
        help_text='Fragment of proper site name not including BHP protocol number or location'
        )

    local_title = models.CharField(max_length=25, blank=True)

    funding_source = models.ManyToManyField(FundingSource)

    date_registered = models.DateField(
        verbose_name="Date registered with BHP",
        )

    date_opened = models.DateField(
        verbose_name="Date opened",
        )

    description = models.TextField(
        max_length=500,
        )

    def __unicode__(self):
        return self.protocol_identifier

    class Meta:
        ordering = ['protocol_identifier']
        app_label = 'bhp_research_protocol'
