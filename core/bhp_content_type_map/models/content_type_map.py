from django.contrib.contenttypes.models import ContentType
from django.db import models

from edc.base.model.models import BaseModel

from ..exceptions import ContentTypeMapError
from ..managers import ContentTypeMapManager


class ContentTypeMap(BaseModel):

    content_type = models.ForeignKey(ContentType,
        verbose_name='Link to content type',
        null=True,
        blank=True,
        )

    app_label = models.CharField(
        max_length=50,
        db_index=True,
        )

    name = models.CharField(
        verbose_name='Model verbose_name',
        max_length=50,
        db_index=True,
        )

    model = models.CharField(
        verbose_name='Model name (module name)',
        max_length=50,
        db_index=True,
        )

    module_name = models.CharField(
        max_length=50,
        null=True,
        )

    objects = ContentTypeMapManager()

    def save(self, *args, **kwargs):
        self.module_name = self.model
        super(ContentTypeMap, self).save(*args, **kwargs)

    def natural_key(self):
        return self.content_type.natural_key()

    def model_class(self):
        if self.content_type.name.lower() != self.name.lower():
            raise ContentTypeMapError('ContentTypeMap is not in sync with ContentType for verbose_name {}. '
                                      'Run sync_content_type management command.'.format(self.name))
        if self.content_type.model != self.model:
            raise ContentTypeMapError('ContentTypeMap is not in sync with ContentType for model {}. '
                                      'Run sync_content_type management command.'.format(self.name))
        return self.content_type.model_class()

    def __unicode__(self):
        return unicode(self.content_type)

    class Meta:
        app_label = 'bhp_content_type_map'
        unique_together = ['app_label', 'model', ]
        ordering = ['name', ]
