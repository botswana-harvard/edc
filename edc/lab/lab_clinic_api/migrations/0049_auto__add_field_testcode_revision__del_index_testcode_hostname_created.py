# -*- coding: utf-8 -*-
import datetime
from south.db import db
from south.v2 import SchemaMigration
from django.db import models


class Migration(SchemaMigration):

    def forwards(self, orm):
        # Adding field 'TestCode.revision'
        db.add_column(u'lab_clinic_api_testcode', 'revision',
                      self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True),
                      keep_default=False)

        # Changing field 'TestCode.user_modified'
        db.alter_column(u'lab_clinic_api_testcode', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'TestCode', fields ['user_modified']

        # Changing field 'TestCode.user_created'
        db.alter_column(u'lab_clinic_api_testcode', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'TestCode', fields ['user_created']

        # Changing field 'AliquotType.user_modified'
        db.alter_column(u'lab_clinic_api_aliquottype', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=50))

        # Changing field 'AliquotType.user_created'
        db.alter_column(u'lab_clinic_api_aliquottype', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'AliquotType', fields ['user_created']

        # Changing field 'Review.user_modified'
        db.alter_column(u'lab_clinic_api_review', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'Review', fields ['user_modified']

        # Changing field 'Review.user_created'
        db.alter_column(u'lab_clinic_api_review', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'Review', fields ['user_created']

        # Changing field 'Panel.user_modified'
        db.alter_column(u'lab_clinic_api_panel', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'Panel', fields ['user_modified']

        # Changing field 'Panel.user_created'
        db.alter_column(u'lab_clinic_api_panel', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'Panel', fields ['user_created']

        # Changing field 'AliquotCondition.user_modified'
        db.alter_column(u'lab_clinic_api_aliquotcondition', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'AliquotCondition', fields ['user_modified']

        # Changing field 'AliquotCondition.user_created'
        db.alter_column(u'lab_clinic_api_aliquotcondition', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'AliquotCondition', fields ['user_created']

        # Changing field 'Order.user_modified'
        db.alter_column(u'lab_clinic_api_order', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'Order', fields ['user_modified']

        # Changing field 'Order.user_created'
        db.alter_column(u'lab_clinic_api_order', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'Order', fields ['user_created']


        # Adding field 'TestCodeGroup.revision'
        db.add_column(u'lab_clinic_api_testcodegroup', 'revision',
                      self.gf('django.db.models.fields.CharField')(max_length=75, null=True, blank=True),
                      keep_default=False)

        # Changing field 'TestCodeGroup.user_modified'
        db.alter_column(u'lab_clinic_api_testcodegroup', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=50))
 
        # Changing field 'TestCodeGroup.user_created'
        db.alter_column(u'lab_clinic_api_testcodegroup', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=50))
        # Removing index on 'TestCodeGroup', fields ['user_created']

    def backwards(self, orm):
        raise TypeError()
        # Adding index on 'TestCodeGroup', fields ['user_created']
        db.create_index(u'lab_clinic_api_testcodegroup', ['user_created'])

        # Adding index on 'TestCodeGroup', fields ['hostname_modified']
        db.create_index(u'lab_clinic_api_testcodegroup', ['hostname_modified'])

        # Adding index on 'TestCodeGroup', fields ['user_modified']
        db.create_index(u'lab_clinic_api_testcodegroup', ['user_modified'])

        # Adding index on 'TestCodeGroup', fields ['hostname_created']
        db.create_index(u'lab_clinic_api_testcodegroup', ['hostname_created'])

        # Adding index on 'Order', fields ['user_created']
        db.create_index(u'lab_clinic_api_order', ['user_created'])

        # Adding index on 'Order', fields ['hostname_modified']
        db.create_index(u'lab_clinic_api_order', ['hostname_modified'])

        # Adding index on 'Order', fields ['user_modified']
        db.create_index(u'lab_clinic_api_order', ['user_modified'])

        # Adding index on 'Order', fields ['hostname_created']
        db.create_index(u'lab_clinic_api_order', ['hostname_created'])

        # Adding index on 'AliquotCondition', fields ['user_created']
        db.create_index(u'lab_clinic_api_aliquotcondition', ['user_created'])

        # Adding index on 'AliquotCondition', fields ['hostname_created']
        db.create_index(u'lab_clinic_api_aliquotcondition', ['hostname_created'])

        # Adding index on 'AliquotCondition', fields ['user_modified']
        db.create_index(u'lab_clinic_api_aliquotcondition', ['user_modified'])

        # Adding index on 'AliquotCondition', fields ['hostname_modified']
        db.create_index(u'lab_clinic_api_aliquotcondition', ['hostname_modified'])

        # Adding index on 'Panel', fields ['user_created']
        db.create_index(u'lab_clinic_api_panel', ['user_created'])

        # Adding index on 'Panel', fields ['hostname_modified']
        db.create_index(u'lab_clinic_api_panel', ['hostname_modified'])

        # Adding index on 'Panel', fields ['user_modified']
        db.create_index(u'lab_clinic_api_panel', ['user_modified'])

        # Adding index on 'Panel', fields ['hostname_created']
        db.create_index(u'lab_clinic_api_panel', ['hostname_created'])

        # Adding index on 'Review', fields ['user_created']
        db.create_index(u'lab_clinic_api_review', ['user_created'])

        # Adding index on 'Review', fields ['hostname_modified']
        db.create_index(u'lab_clinic_api_review', ['hostname_modified'])

        # Adding index on 'Review', fields ['user_modified']
        db.create_index(u'lab_clinic_api_review', ['user_modified'])

        # Adding index on 'Review', fields ['hostname_created']
        db.create_index(u'lab_clinic_api_review', ['hostname_created'])

        # Adding index on 'AliquotType', fields ['user_created']
        db.create_index(u'lab_clinic_api_aliquottype', ['user_created'])

        # Adding index on 'AliquotType', fields ['hostname_modified']
        db.create_index(u'lab_clinic_api_aliquottype', ['hostname_modified'])

        # Adding index on 'AliquotType', fields ['user_modified']
        db.create_index(u'lab_clinic_api_aliquottype', ['user_modified'])

        # Adding index on 'AliquotType', fields ['hostname_created']
        db.create_index(u'lab_clinic_api_aliquottype', ['hostname_created'])

        # Adding index on 'TestCode', fields ['user_created']
        db.create_index(u'lab_clinic_api_testcode', ['user_created'])

        # Adding index on 'TestCode', fields ['hostname_modified']
        db.create_index(u'lab_clinic_api_testcode', ['hostname_modified'])

        # Adding index on 'TestCode', fields ['user_modified']
        db.create_index(u'lab_clinic_api_testcode', ['user_modified'])

        # Adding index on 'TestCode', fields ['hostname_created']
        db.create_index(u'lab_clinic_api_testcode', ['hostname_created'])

        # Deleting field 'TestCode.revision'
        db.delete_column(u'lab_clinic_api_testcode', 'revision')


        # Changing field 'TestCode.user_modified'
        db.alter_column(u'lab_clinic_api_testcode', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'TestCode.user_created'
        db.alter_column(u'lab_clinic_api_testcode', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=250))
        # Adding field 'Aliquot.hostname_created'
        db.add_column(u'lab_clinic_api_aliquot', 'hostname_created',
                      self.gf('django.db.models.fields.CharField')(default='Tshepisos-MacBook-Pro.local', max_length=50, blank=True, db_index=True),
                      keep_default=False)

        # Adding field 'Aliquot.hostname_modified'
        db.add_column(u'lab_clinic_api_aliquot', 'hostname_modified',
                      self.gf('django.db.models.fields.CharField')(default='Tshepisos-MacBook-Pro.local', max_length=50, blank=True, db_index=True),
                      keep_default=False)

        # Adding field 'Aliquot.user_created'
        db.add_column(u'lab_clinic_api_aliquot', 'user_created',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'Aliquot.user_modified'
        db.add_column(u'lab_clinic_api_aliquot', 'user_modified',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'Aliquot.revision'
        db.add_column(u'lab_clinic_api_aliquot', 'revision',
                      self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Aliquot.created'
        db.add_column(u'lab_clinic_api_aliquot', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'Aliquot.modified'
        db.add_column(u'lab_clinic_api_aliquot', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)


        # Changing field 'Aliquot.id'
        db.alter_column(u'lab_clinic_api_aliquot', 'id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True))
        # Deleting field 'AliquotType.revision'
        db.delete_column(u'lab_clinic_api_aliquottype', 'revision')


        # Changing field 'AliquotType.user_modified'
        db.alter_column(u'lab_clinic_api_aliquottype', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'AliquotType.user_created'
        db.alter_column(u'lab_clinic_api_aliquottype', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Review.user_modified'
        db.alter_column(u'lab_clinic_api_review', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Review.user_created'
        db.alter_column(u'lab_clinic_api_review', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Review.revision'
        db.alter_column(u'lab_clinic_api_review', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
        # Deleting field 'Panel.revision'
        db.delete_column(u'lab_clinic_api_panel', 'revision')


        # Changing field 'Panel.user_modified'
        db.alter_column(u'lab_clinic_api_panel', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Panel.user_created'
        db.alter_column(u'lab_clinic_api_panel', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=250))
        # Adding field 'Receive.hostname_created'
        db.add_column(u'lab_clinic_api_receive', 'hostname_created',
                      self.gf('django.db.models.fields.CharField')(default='Tshepisos-MacBook-Pro.local', max_length=50, blank=True, db_index=True),
                      keep_default=False)

        # Adding field 'Receive.created'
        db.add_column(u'lab_clinic_api_receive', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'Receive.user_modified'
        db.add_column(u'lab_clinic_api_receive', 'user_modified',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'Receive.hostname_modified'
        db.add_column(u'lab_clinic_api_receive', 'hostname_modified',
                      self.gf('django.db.models.fields.CharField')(default='Tshepisos-MacBook-Pro.local', max_length=50, blank=True, db_index=True),
                      keep_default=False)

        # Adding field 'Receive.modified'
        db.add_column(u'lab_clinic_api_receive', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'Receive.user_created'
        db.add_column(u'lab_clinic_api_receive', 'user_created',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'Receive.revision'
        db.add_column(u'lab_clinic_api_receive', 'revision',
                      self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True),
                      keep_default=False)


        # Changing field 'Receive.id'
        db.alter_column(u'lab_clinic_api_receive', 'id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True))
        # Deleting field 'AliquotCondition.revision'
        db.delete_column(u'lab_clinic_api_aliquotcondition', 'revision')


        # Changing field 'AliquotCondition.user_modified'
        db.alter_column(u'lab_clinic_api_aliquotcondition', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'AliquotCondition.user_created'
        db.alter_column(u'lab_clinic_api_aliquotcondition', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Order.user_modified'
        db.alter_column(u'lab_clinic_api_order', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Order.user_created'
        db.alter_column(u'lab_clinic_api_order', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'Order.revision'
        db.alter_column(u'lab_clinic_api_order', 'revision', self.gf('django.db.models.fields.CharField')(max_length=150, null=True))
        # Adding field 'Result.hostname_created'
        db.add_column(u'lab_clinic_api_result', 'hostname_created',
                      self.gf('django.db.models.fields.CharField')(default='Tshepisos-MacBook-Pro.local', max_length=50, blank=True, db_index=True),
                      keep_default=False)

        # Adding field 'Result.hostname_modified'
        db.add_column(u'lab_clinic_api_result', 'hostname_modified',
                      self.gf('django.db.models.fields.CharField')(default='Tshepisos-MacBook-Pro.local', max_length=50, blank=True, db_index=True),
                      keep_default=False)

        # Adding field 'Result.user_created'
        db.add_column(u'lab_clinic_api_result', 'user_created',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'Result.user_modified'
        db.add_column(u'lab_clinic_api_result', 'user_modified',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'Result.revision'
        db.add_column(u'lab_clinic_api_result', 'revision',
                      self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True),
                      keep_default=False)

        # Adding field 'Result.created'
        db.add_column(u'lab_clinic_api_result', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'Result.modified'
        db.add_column(u'lab_clinic_api_result', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)


        # Changing field 'Result.id'
        db.alter_column(u'lab_clinic_api_result', 'id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True))
        # Deleting field 'TestCodeGroup.revision'
        db.delete_column(u'lab_clinic_api_testcodegroup', 'revision')


        # Changing field 'TestCodeGroup.user_modified'
        db.alter_column(u'lab_clinic_api_testcodegroup', 'user_modified', self.gf('django.db.models.fields.CharField')(max_length=250))

        # Changing field 'TestCodeGroup.user_created'
        db.alter_column(u'lab_clinic_api_testcodegroup', 'user_created', self.gf('django.db.models.fields.CharField')(max_length=250))
        # Adding field 'ResultItem.hostname_created'
        db.add_column(u'lab_clinic_api_resultitem', 'hostname_created',
                      self.gf('django.db.models.fields.CharField')(default='Tshepisos-MacBook-Pro.local', max_length=50, blank=True, db_index=True),
                      keep_default=False)

        # Adding field 'ResultItem.user_modified'
        db.add_column(u'lab_clinic_api_resultitem', 'user_modified',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'ResultItem.hostname_modified'
        db.add_column(u'lab_clinic_api_resultitem', 'hostname_modified',
                      self.gf('django.db.models.fields.CharField')(default='Tshepisos-MacBook-Pro.local', max_length=50, blank=True, db_index=True),
                      keep_default=False)

        # Adding field 'ResultItem.user_created'
        db.add_column(u'lab_clinic_api_resultitem', 'user_created',
                      self.gf('django.db.models.fields.CharField')(default='', max_length=250, db_index=True),
                      keep_default=False)

        # Adding field 'ResultItem.created'
        db.add_column(u'lab_clinic_api_resultitem', 'created',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'ResultItem.modified'
        db.add_column(u'lab_clinic_api_resultitem', 'modified',
                      self.gf('django.db.models.fields.DateTimeField')(default=datetime.datetime.now, blank=True),
                      keep_default=False)

        # Adding field 'ResultItem.revision'
        db.add_column(u'lab_clinic_api_resultitem', 'revision',
                      self.gf('django.db.models.fields.CharField')(max_length=150, null=True, blank=True),
                      keep_default=False)


        # Changing field 'ResultItem.id'
        db.alter_column(u'lab_clinic_api_resultitem', 'id', self.gf('django.db.models.fields.CharField')(max_length=36, primary_key=True))

    models = {
        'bhp_variables.studysite': {
            'Meta': {'ordering': "['site_code']", 'unique_together': "[('site_code', 'site_name')]", 'object_name': 'StudySite'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'site_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '4'}),
            'site_name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '35'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'lab_clinic_api.aliquot': {
            'Meta': {'ordering': "('receive', 'count')", 'unique_together': "(('receive', 'count'),)", 'object_name': 'Aliquot'},
            'aliquot_condition': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.AliquotCondition']", 'null': 'True', 'blank': 'True'}),
            'aliquot_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 19, 0, 0)'}),
            'aliquot_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25'}),
            'aliquot_type': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.AliquotType']", 'null': 'True'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'count': ('django.db.models.fields.IntegerField', [], {'null': 'True'}),
            'current_measure': ('django.db.models.fields.DecimalField', [], {'default': "'5.00'", 'max_digits': '10', 'decimal_places': '2'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'is_packed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'measure_units': ('django.db.models.fields.CharField', [], {'default': "'mL'", 'max_length': '25'}),
            'medium': ('django.db.models.fields.CharField', [], {'default': "'TUBE'", 'max_length': '25'}),
            'original_measure': ('django.db.models.fields.DecimalField', [], {'default': "'5.00'", 'max_digits': '10', 'decimal_places': '2'}),
            'primary_aliquot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'primary'", 'null': 'True', 'to': "orm['lab_clinic_api.Aliquot']"}),
            'receive': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.Receive']"}),
            'receive_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'source_aliquot': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'source'", 'null': 'True', 'to': "orm['lab_clinic_api.Aliquot']"}),
            'status': ('django.db.models.fields.CharField', [], {'default': "'available'", 'max_length': '25'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'})
        },
        'lab_clinic_api.aliquotcondition': {
            'Meta': {'object_name': 'AliquotCondition'},
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_index': ('django.db.models.fields.IntegerField', [], {'default': '0', 'db_index': 'True'}),
            'field_name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'short_name': ('django.db.models.fields.CharField', [], {'max_length': '250', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'version': ('django.db.models.fields.CharField', [], {'default': "'1.0'", 'max_length': '35'})
        },
        'lab_clinic_api.aliquottype': {
            'Meta': {'ordering': "['name']", 'object_name': 'AliquotType'},
            'alpha_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'numeric_code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '2'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'lab_clinic_api.order': {
            'Meta': {'ordering': "['order_identifier']", 'object_name': 'Order'},
            'aliquot': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.Aliquot']"}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'import_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'order_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'order_identifier': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '25', 'db_index': 'True'}),
            'panel': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.Panel']"}),
            'receive_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'lab_clinic_api.panel': {
            'Meta': {'object_name': 'Panel'},
            'aliquot_type': ('django.db.models.fields.related.ManyToManyField', [], {'to': "orm['lab_clinic_api.AliquotType']", 'symmetrical': 'False'}),
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '250', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'edc_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '50', 'db_index': 'True'}),
            'panel_type': ('django.db.models.fields.CharField', [], {'default': "'TEST'", 'max_length': '15'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'test_code': ('django.db.models.fields.related.ManyToManyField', [], {'symmetrical': 'False', 'to': "orm['lab_clinic_api.TestCode']", 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'lab_clinic_api.receive': {
            'Meta': {'object_name': 'Receive'},
            'clinician_initials': ('django.db.models.fields.CharField', [], {'max_length': '3'}),
            'drawn_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'receive_condition': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'receive_datetime': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime(2015, 9, 19, 0, 0)', 'db_index': 'True'}),
            'receive_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'unique': 'True', 'null': 'True', 'db_index': 'True'}),
            'registered_subject': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['registration.RegisteredSubject']", 'null': 'True'}),
            'requisition_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'visit': ('django.db.models.fields.CharField', [], {'max_length': '25'})
        },
        'lab_clinic_api.result': {
            'Meta': {'ordering': "['result_identifier']", 'object_name': 'Result'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'dmis_result_guid': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'order': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.Order']"}),
            'receive_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'release_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'release_status': ('django.db.models.fields.CharField', [], {'default': "'NEW'", 'max_length': '25', 'db_index': 'True'}),
            'release_username': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'result_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'result_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'review': ('django.db.models.fields.related.OneToOneField', [], {'to': "orm['lab_clinic_api.Review']", 'unique': 'True', 'null': 'True'}),
            'reviewed': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'})
        },
        'lab_clinic_api.resultitem': {
            'Meta': {'ordering': "('-result_item_datetime',)", 'object_name': 'ResultItem'},
            'comment': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'error_code': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'grade_flag': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'grade_message': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'grade_range': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'grade_warn': ('django.db.models.fields.BooleanField', [], {'default': 'False'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'import_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'receive_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'reference_flag': ('django.db.models.fields.CharField', [], {'max_length': '5', 'null': 'True', 'blank': 'True'}),
            'reference_range': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'result': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.Result']"}),
            'result_item_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True'}),
            'result_item_operator': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'result_item_quantifier': ('django.db.models.fields.CharField', [], {'default': "'='", 'max_length': '25'}),
            'result_item_value': ('django.db.models.fields.CharField', [], {'max_length': '25', 'db_index': 'True'}),
            'result_item_value_as_float': ('django.db.models.fields.FloatField', [], {'null': 'True', 'db_index': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'test_code': ('django.db.models.fields.related.ForeignKey', [], {'related_name': "'+'", 'to': "orm['lab_clinic_api.TestCode']"}),
            'validation_datetime': ('django.db.models.fields.DateTimeField', [], {'db_index': 'True', 'null': 'True', 'blank': 'True'}),
            'validation_reference': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'blank': 'True'}),
            'validation_status': ('django.db.models.fields.CharField', [], {'default': "'P'", 'max_length': '10', 'db_index': 'True'}),
            'validation_username': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'max_length': '50', 'null': 'True', 'blank': 'True'})
        },
        'lab_clinic_api.review': {
            'Meta': {'ordering': "['review_datetime']", 'object_name': 'Review'},
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '500', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'review_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True'}),
            'review_status': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'title': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'lab_clinic_api.testcode': {
            'Meta': {'ordering': "['edc_name']", 'object_name': 'TestCode'},
            'code': ('django.db.models.fields.CharField', [], {'unique': 'True', 'max_length': '15'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'display_decimal_places': ('django.db.models.fields.IntegerField', [], {'null': 'True', 'blank': 'True'}),
            'edc_code': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'db_index': 'True'}),
            'edc_name': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'formula': ('django.db.models.fields.CharField', [], {'max_length': "'50'", 'null': 'True', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'is_absolute': ('django.db.models.fields.CharField', [], {'default': "'absolute'", 'max_length': "'15'"}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'test_code_group': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['lab_clinic_api.TestCodeGroup']", 'null': 'True'}),
            'units': ('django.db.models.fields.CharField', [], {'max_length': '25'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'lab_clinic_api.testcodegroup': {
            'Meta': {'ordering': "['code']", 'object_name': 'TestCodeGroup'},
            'code': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            u'id': ('django.db.models.fields.AutoField', [], {'primary_key': 'True'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'name': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        },
        'registration.registeredsubject': {
            'Meta': {'ordering': "['subject_identifier']", 'unique_together': "(('first_name', 'dob', 'initials', 'additional_key'),)", 'object_name': 'RegisteredSubject', 'db_table': "'bhp_registration_registeredsubject'"},
            'additional_key': ('django.db.models.fields.CharField', [], {'default': 'None', 'max_length': '36', 'null': 'True'}),
            'comment': ('django.db.models.fields.TextField', [], {'max_length': '250', 'null': 'True', 'blank': 'True'}),
            'created': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'dm_comment': ('django.db.models.fields.CharField', [], {'max_length': '150', 'null': 'True'}),
            'dob': ('django.db.models.fields.DateField', [], {'null': 'True'}),
            'first_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'gender': ('django.db.models.fields.CharField', [], {'max_length': '1', 'null': 'True'}),
            'hiv_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'hostname_created': ('django.db.models.fields.CharField', [], {'default': "'One-2.local'", 'max_length': '50'}),
            'hostname_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'id': ('django.db.models.fields.CharField', [], {'max_length': '36', 'primary_key': 'True'}),
            'identity': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True', 'blank': 'True'}),
            'identity_type': ('django.db.models.fields.CharField', [], {'max_length': '15'}),
            'initials': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'is_dob_estimated': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'last_name': ('django.db.models.fields.CharField', [], {'max_length': '78L', 'null': 'True'}),
            'may_store_samples': ('django.db.models.fields.CharField', [], {'default': "'?'", 'max_length': '3'}),
            'modified': ('django.db.models.fields.DateTimeField', [], {'default': 'datetime.datetime.now', 'blank': 'True'}),
            'randomization_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'registration_identifier': ('django.db.models.fields.CharField', [], {'max_length': '36', 'null': 'True', 'blank': 'True'}),
            'registration_status': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'relative_identifier': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True', 'blank': 'True'}),
            'revision': ('django.db.models.fields.CharField', [], {'max_length': '75', 'null': 'True', 'blank': 'True'}),
            'salt': ('django.db.models.fields.CharField', [], {'default': "'salt'", 'max_length': '25', 'null': 'True'}),
            'screening_datetime': ('django.db.models.fields.DateTimeField', [], {'null': 'True', 'blank': 'True'}),
            'sid': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True', 'blank': 'True'}),
            'study_site': ('django.db.models.fields.related.ForeignKey', [], {'to': "orm['bhp_variables.StudySite']", 'null': 'True', 'blank': 'True'}),
            'subject_consent_id': ('django.db.models.fields.CharField', [], {'max_length': '100', 'null': 'True', 'blank': 'True'}),
            'subject_identifier': ('django.db.models.fields.CharField', [], {'db_index': 'True', 'unique': 'True', 'max_length': '50', 'blank': 'True'}),
            'subject_identifier_aka': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True'}),
            'subject_identifier_as_pk': ('django.db.models.fields.CharField', [], {'max_length': '50', 'null': 'True', 'db_index': 'True'}),
            'subject_type': ('django.db.models.fields.CharField', [], {'max_length': '25', 'null': 'True'}),
            'survival_status': ('django.db.models.fields.CharField', [], {'max_length': '15', 'null': 'True'}),
            'user_created': ('django.db.models.fields.CharField', [], {'max_length': '50'}),
            'user_modified': ('django.db.models.fields.CharField', [], {'max_length': '50'})
        }
    }

    complete_apps = ['lab_clinic_api']