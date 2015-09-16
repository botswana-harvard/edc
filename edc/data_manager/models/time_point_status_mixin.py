from django.db import models

from .time_point_status import TimePointStatus


class TimePointStatusMixin(models.Model):

    def save(self, *args, **kwargs):
        # TimePointStatus = models.get_model('data_manager', 'TimePointStatus')
        using = kwargs.get('using')
        if self.id:
            try:
                TimePointStatus.check_time_point_status(
                    self.get_visit().appointment, using=using)
            except AttributeError:
                TimePointStatus.check_time_point_status(self.appointment, using=using)
        if 'is_off_study' in dir(self):
            if self.is_off_study():
                raise ValueError(
                    'Model cannot be saved. Subject is off study. Perhaps catch '
                    'this exception in forms clean() method.')
        super(TimePointStatusMixin, self).save(*args, **kwargs)

    class Meta:
        abstract = True
