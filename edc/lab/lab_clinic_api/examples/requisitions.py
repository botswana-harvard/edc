import pyodbc

from django.conf import settings

from edc.apps.bcpp_lab.models import SubjectRequisition


cnxn2 = pyodbc.connect(settings.LAB_IMPORT_DMIS_DATA_SOURCE)
cursor = cnxn2.cursor()
sql = "select * from BHPLAB.DBO.LAB01Response where sample_protocolnumber='BHP066'"
results = {}


#fetch all receiving records from BHPLAB
for row in cursor.execute(str(sql)):
    results.update({row.edc_specimen_identifier: (row.PID, row.PAT_ID, row.edc_specimen_identifier, row.TID, row.headerdate)})

print results

# for each requisition, is there a corresponding receiving record
for requisition in SubjectRequisition.objects.filter(is_receive=True):
    if not requisition.specimen_identifier in results:
        print '", "'.join([requisition.subject_visit.get_subject_identifier(), requisition.specimen_identifier, unicode(requisition.panel)])

for key, value in results.iteritems():
    if not SubjectRequisition.objects.filter(specimen_identifier=key):
        print '", "'.join([value[1], value[0], value[2], value[3], value[4]])


from collections import OrderedDict
from django.db.models import get_app, get_models

app = get_app('bcpp_subject')
dd = OrderedDict()

for model in get_models(app):
    dd[model._meta.db_table] = {}
    for field in model._meta.fields:
        dd[model._meta.db_table].update({'table': model._meta.db_table,
                                         'name': field.name,
                                         'type': '',
                                         'blank': field.blank,
                                         'null': field.null,
                                         'max_length': field.max_length,
                                         'editable': field.editable,
                                         'unique': field._unique,
                                         'prompt': field.verbose_name})
