import factory
from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from edc.core.bhp_variables.tests.factories import StudySiteFactory
from edc.lab.lab_clinic_api.tests.factories import AliquotTypeFactory, PanelFactory


class BaseBaseRequisitionFactory(BaseUuidModelFactory):
    ABSTRACT_FACTORY = True

    requisition_identifier = factory.Sequence(lambda n: n.rjust(8, '0'))
    requisition_datetime = datetime.today()
    site = factory.SubFactory(StudySiteFactory)
    aliquot_type = factory.SubFactory(AliquotTypeFactory)
    panel = factory.SubFactory(PanelFactory)
    drawn_datetime = datetime.today()
