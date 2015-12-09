from django.db import models, transaction

from edc.subject.visit_schedule.models.visit_definition import VisitDefinition


class PreviousVisitError(Exception):
    pass


class PreviousVisitMixin(models.Model):

    """A mixin to force the user to complete visits in sequence.

    * Ensures the previous visit exists before allowing save() by raising PreviousVisitError.
    * If the visit is the first in the sequence, save() is allowed.
    * If REQUIRES_PREVIOUS_VISIT = False, mixin is disabled.

    For example:

        class TestVisit(MetaDataMixin, PreviousVisitMixin, BaseVisitTracking):

            REQUIRES_PREVIOUS_VISIT = True

            def custom_post_update_entry_meta_data(self):
                pass

            class Meta:
                app_label = 'my_app'

    """

    REQUIRES_PREVIOUS_VISIT = True

    def save(self, *args, **kwargs):
        if not self.has_previous_visit():
            raise PreviousVisitError('Previous visit report is not complete.')
        super(PreviousVisitMixin, self).save(*args, **kwargs)

    def previous_visit_definition(self, code):
        """Returns the previous visit definition relative to this instance or None."""
        visit_definition = VisitDefinition.objects.get(code=code)
        previous_visit_definition = VisitDefinition.objects.filter(
            time_point__lt=visit_definition.time_point).order_by('time_point', 'base_interval').first()
        if previous_visit_definition:
            return previous_visit_definition
        return None

    def previous_visit(self):
        """Returns the previous visit if it exists."""
        with transaction.atomic():
            try:
                code = self.appointment.visit_definition.code
                previous_visit = self.__class__.objects.get(
                    appointment__visit_definition=self.previous_visit_definition(code))
            except self.__class__.DoesNotExist:
                previous_visit = None
        return previous_visit

    def has_previous_visit(self):
        """Returns True if the previous visit in the schedule exists or this is the first visit.

        Is by-passed if REQUIRES_PREVIOUS_VISIT is False. """
        if not self.REQUIRES_PREVIOUS_VISIT:
            return True
        if self.previous_visit():
            has_previous_visit = True
        elif (self.appointment.visit_definition.time_point == 0 and
                self.appointment.visit_definition.base_interval == 0):
            has_previous_visit = True
        else:
            has_previous_visit = False
        return has_previous_visit

    class Meta:
        abstract = True
