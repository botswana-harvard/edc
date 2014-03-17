

class LabProfile(object):

    name = None
    profile_group_name = None  # controller uses this to register the aliquot, receive, ... models so they can be referenced by the group name
    receive_model = None
    panel_model = None
    aliquot_model = None
    aliquot_type_model = None
    profile_model = None
    profile_item_model = None
    requisition_model = None

    def receive(self, requisition):
        """Receives a specimen and creates the primary aliqout based on the requisition."""
        received = False
        if requisition.is_drawn.lower() == 'yes':
            if not self.receive_model.objects.filter(receive_identifier=requisition.specimen_identifier):
                # capture basic info on specimen
                receive = self.receive_model.objects.create(
                    registered_subject=requisition.get_visit().appointment.registered_subject,
                    receive_identifier=requisition.specimen_identifier,
                    requisition_identifier=requisition.requisition_identifier,
                    drawn_datetime=requisition.drawn_datetime,
                    visit=requisition.get_visit().appointment.visit_definition.code)
            else:
                receive = self.receive_model.objects.get(receive_identifier=requisition.specimen_identifier)
            if not self.aliquot_model.objects.filter(receive=receive):
                # create primary aliquot
                aliquot = self.aliquot_model.objects.create(
                    primary_aliquot=None,
                    source_aliquot=None,
                    receive=receive,
                    count=0,
                    aliquot_type=requisition.aliquot_type,
                    aliquot_condition=None)
                aliquot.primary_aliquot = aliquot
                aliquot.aliquot_identifier = self.aliquot_identifier(aliquot, requisition.aliquot_type, 1)
                aliquot.save()
            received = True
        return received

    def aliquot(self, source_aliquot, aliquot_type, count):
        """Creates aliquots from the source and increments the aliquot count from the existing primary."""
        aliquot_count = self.aliquot_model.objects.filter(receive=source_aliquot.receive).count()
        for _ in range(count):
            aliquot_count = aliquot_count + 1
            self.aliquot_model.objects.create(
                aliquot_identifier=self.aliquot_identifier(source_aliquot, aliquot_type, aliquot_count),
                primary_aliquot=source_aliquot.primary_aliquot,
                source_aliquot=source_aliquot,
                count=aliquot_count,
                receive=source_aliquot.receive,
                aliquot_type=aliquot_type,
                aliquot_condition=None)

    def aliquot_by_profile(self, source_aliquot, profile):
        """Create aliquots as per the profile."""
        for obj in self.profile_item_model.objects.filter(profile=profile):
            self.aliquot(source_aliquot, obj.aliquot_type, obj.count)

    def aliquot_identifier(self, source_aliquot, aliquot_type, aliquot_count):
        aliquot_stub = '{0}{1}'.format(aliquot_type.numeric_code.zfill(2), str(aliquot_count).zfill(2))
        return '{0}{1}'.format(source_aliquot.receive.receive_identifier, aliquot_stub)
