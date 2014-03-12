from ..models import Receive, Aliquot


class SpecimenHelper(object):
    def receive(self, requisition):
        """Receives a specimen and creates a corresponding aliqout based on the requisition."""
        received = False
        if not Receive.objects.filter(receive_identifier=requisition.specimen_identifier):
            receive = Receive.objects.create(
                registered_subject=requisition.get_visit().appointment.registered_subject,
                receive_identifier=requisition.specimen_identifier,
                requisition_identifier=requisition.requisition_identifier,
                drawn_datetime=requisition.drawn_datetime,
                visit=requisition.get_visit().appointment.visit_definition.code)
            if not Aliquot.objects.filter(receive=receive):
                Aliquot.objects.create(
                    receive=receive,
                    aliquot_type=requisition.aliquot_type,
                    aliquot_condition=None)
            received = True
        return received
