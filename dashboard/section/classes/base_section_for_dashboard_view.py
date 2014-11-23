from .base_section_view import BaseSectionView


class BaseSectionForDashboardView(BaseSectionView):

    """Adds dashboard url methods to section views that show links to a dashboard."""

    dashboard_url_name = None

    def contribute_to_context(self, context, request, *args, **kwargs):
        """Adds subject_dashboard_url to the context."""
#         context = super(BaseSectionForDashboardView, self)._contribute_to_context(context, request, *args, **kwargs)
        context.update({'subject_dashboard_url': self.dashboard_url_name})
        return context
