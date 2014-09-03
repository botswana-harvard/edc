from django.db import models
from django.contrib.contenttypes.models import ContentType


class ContentTypeMapManager(models.Manager):

    def get_by_natural_key(self, app_label, model):
        content_type = ContentType.objects.get_by_natural_key(app_label, model)
        return self.get(content_type=content_type)
