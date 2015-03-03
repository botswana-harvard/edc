from django.db import models


class ShortenName():

    original_name = models.CharField(
        verbose_name=_('Original name.'),
        max_length=50,
        unique=True)

    shorter_name = models.CharField(
        verbose_name=_('Shorter version of original name.'),
        max_length=50)

    objects = models.Manager()