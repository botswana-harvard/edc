from ..models import Receive, Aliquot, ProcessingProfileItem


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
                    aliquot.save()
                received = True
        return received

    def aliquot(self, source_aliquot, aliquot_type, count):
        """Creates aliquots from the source and increments the aliquot count from the existing primary."""
        aliquot_count = Aliquot.objects.filter(receive=source_aliquot.receive).count()
        for i in range(count):
            aliquot_count = aliquot_count + i,
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
        for obj in ProcessingProfileItem.objects.filter(processing_profile=processing_profile, aliquot_type=source_aliquot.aliquot_type):
            self.aliquot(source_aliquot, obj.aliquot_type, obj.count)

    def aliquot_identifier(self, source_aliquot, aliquot_type, aliquot_count):
        if not source_aliquot.source_aliquot:
            source_stub = '0000'
        else:
            source_stub = '{0}{1}'.format(source_aliquot.source_aliquot.aliquot_type.numeric_code, source_aliquot.source_aliquot.aliquot_count)
        aliquot_stub = '{0}{1}'.format(aliquot_type.numeric_code, aliquot_count)
        return '{0}{1}{2}'.format(source_aliquot.receive.receive_identifier, source_stub, aliquot_stub)
