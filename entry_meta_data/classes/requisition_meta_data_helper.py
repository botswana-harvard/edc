from edc.subject.entry.models import LabEntry

from ..models import RequisitionMetaData

from .base_meta_data_helper import BaseMetaDataHelper


class RequisitionMetaDataHelper(BaseMetaDataHelper):

    meta_data_model = RequisitionMetaData
    entry_model = LabEntry
    entry_attr = 'lab_entry'