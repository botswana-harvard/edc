from django.db import models


class Subject(models.Model):
    """Base for registered subject models."""

    class Meta:
        abstract = True
