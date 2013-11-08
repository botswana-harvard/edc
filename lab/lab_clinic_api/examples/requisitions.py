import pyodbc

from django.conf import settings

from apps.bcpp_lab.models import SubjectRequisition


cnxn2 = pyodbc.connect(settings.LAB_IMPORT_DMIS_DATA_SOURCE)
cursor = cnxn2.cursor()
sql = "select * from BHPLAB.DBO.LAB01Response where sample_protocolnumber='BHP066'"
results = {}

for row in cursor.execute(str(sql)):
    results.update({row.edc_specimen_identifier: (row.PID, row.PAT_ID, row.edc_specimen_identifier, row.TID, row.headerdate)})

for requisition in SubjectRequisition.objects.filter(is_receive=True):
    if not requisition.specimen_identifier in results:
        print '", "'.join([requisition.subject_visit.get_subject_identifier(), requisition.specimen_identifier, unicode(requisition.panel)])

for key, value in results.iteritems():
    if not SubjectRequisition.objects.filter(specimen_identifier=key):
        print '", "'.join([value[1], value[0], value[2], value[3], value[4]])
