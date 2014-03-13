from datetime import datetime

from ..models import Receive, Aliquot, ProcessingProfileItem

from .aliquot_label import AliquotLabel


class SpecimenHelper(object):
    def receive(self, requisition):
        """Receives a specimen and creates the primary aliqout based on the requisition."""
        received = False
        if requisition.is_drawn.lower() == 'yes':
            if not Receive.objects.filter(receive_identifier=requisition.specimen_identifier):
                # capture basic info on specimen
                receive = Receive.objects.create(
                    registered_subject=requisition.get_visit().appointment.registered_subject,
                    receive_identifier=requisition.specimen_identifier,
                    requisition_identifier=requisition.requisition_identifier,
                    drawn_datetime=requisition.drawn_datetime,
                    visit=requisition.get_visit().appointment.visit_definition.code)
            else:
                receive = Receive.objects.get(receive_identifier=requisition.specimen_identifier)
            if not Aliquot.objects.filter(receive=receive):
                # create primary aliquot
                aliquot = Aliquot.objects.create(
                    primary_aliquot=None,
                    source_aliquot=None,
                    receive=receive,
                    aliquot_count=0,
                    aliquot_type=requisition.aliquot_type,
                    aliquot_condition=None)
                aliquot.primary_aliquot = aliquot
                aliquot.aliquot_identifier = self.aliquot_identifier(aliquot, requisition.aliquot_type, 1)
                aliquot.save()
            received = True
        return received

    def aliquot(self, source_aliquot, aliquot_type, count):
        """Creates aliquots from the source and increments the aliquot count from the existing primary."""
        aliquot_count = Aliquot.objects.filter(receive=source_aliquot.receive).count()
        for _ in range(count):
            aliquot_count = aliquot_count + 1
            Aliquot.objects.create(
                aliquot_identifier=self.aliquot_identifier(source_aliquot, aliquot_type, aliquot_count),
                primary_aliquot=source_aliquot.primary_aliquot,
                source_aliquot=source_aliquot,
                aliquot_count=aliquot_count,
                receive=source_aliquot.receive,
                aliquot_type=aliquot_type,
                aliquot_condition=None)

    def aliquot_by_profile(self, source_aliquot, processing_profile):
        """Create aliquots as per the profile."""
        for obj in ProcessingProfileItem.objects.filter(processing_profile=processing_profile):
            self.aliquot(source_aliquot, obj.aliquot_type, obj.count)

    def aliquot_identifier(self, source_aliquot, aliquot_type, aliquot_count):
        aliquot_stub = '{0}{1}'.format(aliquot_type.numeric_code.zfill(2), str(aliquot_count).zfill(2))
        return '{0}{1}'.format(source_aliquot.receive.receive_identifier, aliquot_stub)

    def print_aliquot_label(self, request, aliquot):
        """ Prints a label flags this aliquot as 'labeled'."""
        if aliquot.aliquot_identifier:
            label = AliquotLabel()
            label.print_label(request, aliquot, 1)
            #aliquot.is_labeled = True
            aliquot.modified = datetime.today()
            aliquot.save()
