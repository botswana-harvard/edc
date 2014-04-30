import factory

from datetime import datetime

from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.core.bhp_variables.tests.factories import StudySiteFactory


class BaseBaseRequisitionFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    requisition_identifier = factory.Sequence(lambda n: n.rjust(8, '0'))
    requisition_datetime = datetime.today()
    site = factory.SubFactory(StudySiteFactory)
    drawn_datetime = datetime.today()
