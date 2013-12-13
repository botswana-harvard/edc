from edc.subject.entry.models import Entry

from edc.entry_meta_data.models import ScheduledEntryMetaData
from .base_meta_data_helper import BaseMetaDataHelper


class ScheduledEntryMetaDataHelper(BaseMetaDataHelper):

    meta_data_model = ScheduledEntryMetaData
    entry_model = Entry
    entry_attr = 'entry'
