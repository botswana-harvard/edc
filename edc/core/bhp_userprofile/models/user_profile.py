from django.db import models
from django.contrib.auth.models import User

from edc_base.model.fields import InitialsField

from ..choices import SALUTATION


class UserProfile(models.Model):

    user = models.OneToOneField(User)

    salutation = models.CharField(
        max_length=10,
        choices=SALUTATION,
        default='NONE',)

    initials = InitialsField()

    def __unicode__(self):
        return '%s %s' % (self.user.first_name, self.user.last_name)

    class Meta:
        app_label = 'bhp_userprofile'
