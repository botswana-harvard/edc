from edc.subject.registration.models import RegisteredSubject

from lis.labeling.classes import ModelLabel
from lis.labeling.models import ZplTemplate


class AliquotLabel(ModelLabel):

    def __init__(self):
        super(AliquotLabel, self).__init__()
        template_name = 'aliquot_label'
        if not ZplTemplate.objects.filter(name=template_name):
            template_string = ('^XA\n'
                '^FO325,5^A0N,15,20^FD%(${protocol})s Site %(${site})s^FS\n'
                '^FO320,20^BY1,3.0^BCN,50,N,N,N\n'
                '^BY^FD%(${aliquot_identifier})s^FS\n'
                '^FO320,80^A0N,15,20^FD%(${aliquot_identifier})s^FS\n'
                '^FO325,100^A0N,15,20^FD%(${aliquot_type})s^FS\n'
                '^FO325,118^A0N,16,20^FD%(${subject_identifier})s (%(${initials})s)^FS\n'
                '^FO325,136^A0N,16,20^FDDOB: %(${dob})s %(${gender})s^FS\n'
                '^FO325,152^A0N,20^FD%(${drawn_datetime})s^FS\n'
                '^XZ')
            self.zpl_template = ZplTemplate.objects.create(
                name=template_name,
                template=template_string)
        else:
            self.zpl_template = ZplTemplate.objects.get(name=template_name)

    def refresh_label_context(self):
        aliquot = self.model_instance
        subject_identifier = aliquot.get_subject_identifier()
        registered_subject = RegisteredSubject.objects.get(subject_identifier=subject_identifier)
        custom = {}
        custom.update({
            'aliquot_identifier': aliquot.aliquot_identifier,
            'barcode_value': aliquot.barcode_value(),
            'protocol': aliquot.aliquot_identifier[0:3],
            'site': aliquot.aliquot_identifier[3:5]
            })
#         if 'hiv_status_code' in dir(aliquot):
#             custom.update({'hiv_status_code': str(aliquot.hiv_status_code()), })
#         if 'art_status_code' in dir(aliquot):
#             custom.update({'art_status_code': str(aliquot.art_status_code()), })
        custom.update({
            'drawn_datetime': aliquot.receive.drawn_datetime,
            'subject_identifier': subject_identifier,
            'gender': registered_subject.gender,
            'dob': registered_subject.dob,
            'initials': registered_subject.initials,
            'aliquot_type': aliquot.aliquot_type.alpha_code.upper()})
        self.label_context.update(**custom)
