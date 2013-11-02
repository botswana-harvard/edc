from django.db import models
from django.conf import settings


class UploadFile(models.Model):

    file_path = models.FilePathField()

    file_name = models.FileField(upload_to=settings.MEDIA_ROOT)

    class Meta:
        app_label = 'import'
