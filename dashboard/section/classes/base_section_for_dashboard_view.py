#from django.views.base import View  # for 1.5
from .base_section_view import BaseSectionView


# class Section(View):  # 1.5
class BaseSectionForDashboardView(BaseSectionView):

    """Adds dashboard url methods to section views that show links to a dashboard."""

    dashboard_url_name = None

    def __init__(self):
        self._dashboard_url_name = None
        self.set_dashboard_url_name()
        super(BaseSectionForDashboardView, self).__init__()

    def set_dashboard_url_name(self):
        """Sets the _dashboard_url_name for this section."""
        self._dashboard_url_name = self.dashboard_url_name
        if not self._dashboard_url_name:
            raise TypeError('Attribute dashboard_url_name may not be None for {0}'.format(self))

    def get_dashboard_url_name(self):
        """Returns the _dashboard_url_name for this section."""
        if not self._dashboard_url_name:
            self.set_dashboard_url_name()
        return self._dashboard_url_name

    def _contribute_to_context(self, context, request, *args, **kwargs):
        """Adds subject_dashboard_url to the context.

        .. note:: Overriding this method instead of :func:`contribute_to_context` so that users of the
                  class won't need to call super when overriding :func:`contribute_to_context`."""
        context = super(BaseSectionForDashboardView, self)._contribute_to_context(context, request, *args, **kwargs)
        context.update({'subject_dashboard_url': self.get_dashboard_url_name()})
        return context
