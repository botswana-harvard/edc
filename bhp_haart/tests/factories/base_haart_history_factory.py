from datetime import date
from edc_core.bhp_base_model.tests.factories import BaseUuidModelFactory
from ...choices import ARV_DRUG_LIST


class BaseHaartHistoryFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    arv_code = ARV_DRUG_LIST[0][0]
    date_start = date.today()
