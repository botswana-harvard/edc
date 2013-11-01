import copy
from django.db.models import get_model
from django.core.urlresolvers import reverse
from bhp_common.utils import convert_from_camel
from base_scheduled_entry_context import BaseScheduledEntryContext


class ScheduledEntryContext(BaseScheduledEntryContext):

    """A Class used by the dashboard when rendering the list of scheduled entries to display under "Scheduled Forms"."""

    pass
