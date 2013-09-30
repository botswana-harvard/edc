import factory
from datetime import date
from bhp_base_model.tests.factories import BaseUuidModelFactory
from bhp_haart.choices import ARV_DRUG_LIST, DOSE_STATUS, ARV_MODIFICATION_REASON


class BaseHaartModificationFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    arv_code = ARV_DRUG_LIST[0][0]
    dose_status = DOSE_STATUS[0][0]
    modification_date = date.today()
    modification_code = ARV_MODIFICATION_REASON[0][0]
