import factory

from datetime import datetime

from base.model.tests.factories import BaseUuidModelFactory
from core.bhp_variables.tests.factories import StudySiteFactory


class BaseBaseRequisitionFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    requisition_identifier = factory.Sequence(lambda n: n.rjust(8, '0'))
    requisition_datetime = datetime.today()
    site = factory.SubFactory(StudySiteFactory)
    drawn_datetime = datetime.today()
