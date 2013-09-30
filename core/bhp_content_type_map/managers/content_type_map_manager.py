from django.db import models
from django.contrib.contenttypes.models import ContentType
from ..classes import ContentTypeMapHelper


class ContentTypeMapManager(models.Manager):

    def get_by_natural_key(self, app_label, model):
        content_type = ContentType.objects.get_by_natural_key(app_label, model)
        return self.get(content_type=content_type)

    def sync(self):
        """Syncs content type map foreignkey with django's ContentType id.

        Schema changes might change the key values for records in django's ContentType table.
        Update ContentTypeMap field content_type with the new key."""
        ContentTypeMapHelper().sync()

    def populate(self):
        """Populates ContentTypeMap with django's ContentTypecontent information."""
        ContentTypeMapHelper().populate()
