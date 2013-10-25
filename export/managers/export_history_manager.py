from django.db import models

from ..models import ExportHistory


class ExportHistoryManager(models.Manager):

    def __init__(self, *arg, **kw):
        super(ExportHistoryManager, self).__init__(*arg, **kw)
        self.model = ExportHistory

    def update(self, obj):
        """Update the history model using the exported instance."""
        pass
