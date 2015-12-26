import factory

from datetime import date

from ...choices import ARV_DRUG_LIST


class BaseHaartHistoryFactory(factory.DjangoModelFactory):
    class Meta:
        abstract = True

    arv_code = ARV_DRUG_LIST[0][0]
    date_start = date.today()
