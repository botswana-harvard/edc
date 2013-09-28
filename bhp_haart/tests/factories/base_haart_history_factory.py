import factory
from datetime import date
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_haart.choices import ARV_STATUS_WITH_NEVER, ARV_DRUG_LIST, DOSE_STATUS, ARV_MODIFICATION_REASON


class BaseHaartHistoryFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    arv_code = ARV_DRUG_LIST[0][0]
    date_start = date.today()
