import numpy
from django.db import models
from django.test import SimpleTestCase
from edc.testing.models import TestModel
from ..classes import SupplementalFields


class TestSupplementalFields(SimpleTestCase):

    def test_init(self):
        # only accepts a list or tuple for fields
        fields = 1
        self.assertRaises(AttributeError, SupplementalFields, fields, 0.1)
        fields = 'field'
        self.assertRaises(AttributeError, SupplementalFields, fields, 0.1)
        fields = ['field1', 'field2', 'field3']
        self.assertTrue(isinstance(SupplementalFields(fields, 0.1), SupplementalFields))
        fields = ('field1', 'field2', 'field3')
        self.assertTrue(isinstance(SupplementalFields(fields, 0.1), SupplementalFields))

    def test_set_supplemental_fields(self):
        fields = ('field1', 'field2', 'field3')
        supplemental_fields = SupplementalFields(fields, 0.1)
        self.assertEqual(fields, supplemental_fields._get_supplemental_fields())
        self.assertIsNone(supplemental_fields._set_supplemental_fields(fields))
        self.assertRaises(AttributeError, supplemental_fields._set_supplemental_fields, 1)
        self.assertRaises(AttributeError, supplemental_fields._set_supplemental_fields, 'field1')
        self.assertRaises(AttributeError, supplemental_fields._set_supplemental_fields, None)
        self.assertRaises(AttributeError, supplemental_fields._set_supplemental_fields, [])

    def test_get_supplemental_fields(self):
        fields = ('field1', 'field2', 'field3')
        supplemental_fields = SupplementalFields(fields, 0.1)
        self.assertEqual(supplemental_fields._get_supplemental_fields(), fields)

    def test_set_model_inst(self):
        fields = ('field1', 'field2', 'field3')
        supplemental_fields = SupplementalFields(fields, 0.231)

        class GoodModel(models.Model):
            field1 = models.IntegerField(null=True, blank=False)
            field2 = models.IntegerField(null=True, editable=True)
            field3 = models.IntegerField(null=True)
            field4 = models.IntegerField(null=True)
            field5 = models.IntegerField(null=True)

        model_inst = GoodModel()
        self.assertIsNone(supplemental_fields._set_model_inst(model_inst))
        self.assertEqual(supplemental_fields._model_inst, model_inst)

    def test_get_model_inst(self):
        fields = ('field1', 'field2', 'field3')
        supplemental_fields = SupplementalFields(fields, 0.231)

        class GoodModel(models.Model):
            field1 = models.IntegerField(null=True, blank=False)
            field2 = models.IntegerField(null=True, editable=True)
            field3 = models.IntegerField(null=True)
            field4 = models.IntegerField(null=True)
            field5 = models.IntegerField(null=True)

        model_inst = GoodModel()
        supplemental_fields._set_model_inst(model_inst)
        self.assertEqual(supplemental_fields._get_model_inst(), model_inst)

    def test_set_probability(self):
        # only accepts a float greater than 0 and less than one
        fields = ('field1', 'field2', 'field3')
        self.assertRaises(AttributeError, SupplementalFields, fields, [])
        self.assertRaises(AttributeError, SupplementalFields, fields, ())
        self.assertRaises(AttributeError, SupplementalFields, fields, '0.1')
        self.assertRaises(AttributeError, SupplementalFields, fields, 2)
        self.assertRaises(AttributeError, SupplementalFields, fields, -0.1)
        self.assertRaises(AttributeError, SupplementalFields, fields, 0.12345)
        self.assertTrue(isinstance(SupplementalFields(fields, 0.231), SupplementalFields))

    def test_get_probability(self):
        fields = ('field1', 'field2', 'field3')
        supplemental_fields = SupplementalFields(fields, 0.231)
        self.assertEqual(supplemental_fields._get_probability(), 0.231)

    def test_choose_fields(self):

        class GoodModel(models.Model):
            field1 = models.IntegerField(null=True, blank=False)
            field2 = models.IntegerField(null=True, editable=True)
            field3 = models.IntegerField(null=True)
            field4 = models.IntegerField(null=True)
            field5 = models.IntegerField(null=True)

        supplemental_field_tuple = ('field1', 'field2', 'field3')
        supplemental_fields = SupplementalFields(supplemental_field_tuple, 0.231)
        good_model = GoodModel()
        fields = [fld.name for fld in GoodModel._meta.fields]
        supplemental_fields.choose_fields(fields, good_model)

    def test_check_supplemental_in_original(self):
        fields = ('field1', 'field2', 'field7')
        supplemental_fields = SupplementalFields(fields, 0.231)
        supplemental_fields._set_original_model_admin_fields(('field1', 'field2', 'field3', 'field4', 'field5'))
        self.assertRaises(AttributeError, supplemental_fields._check_supplemental_in_original)
        fields = ('field1', 'field2', 'field3')
        supplimental_fields = SupplementalFields(fields, 0.231)
        supplimental_fields._set_original_model_admin_fields(('field1', 'field2', 'field3', 'field4', 'field5'))
        self.assertTrue(supplimental_fields._check_supplemental_in_original())

    def test_check_supplemental_field_attrs(self):
        fields = ('field1', 'field2', 'field3')
        supplemental_fields = SupplementalFields(fields, 0.231)

        class BadModel1(models.Model):
            field1 = models.IntegerField(editable=False)
            field2 = models.IntegerField()
            field3 = models.IntegerField()
            field4 = models.IntegerField()
            field5 = models.IntegerField()

        self.assertRaises(AttributeError, supplemental_fields._check_supplemental_field_attrs, BadModel1())

        class BadModel2(models.Model):
            field1 = models.IntegerField()
            field2 = models.IntegerField()
            field3 = models.IntegerField()
            field4 = models.IntegerField()
            field5 = models.IntegerField()

        self.assertRaises(AttributeError, supplemental_fields._check_supplemental_field_attrs, BadModel2())

        class BadModel3(models.Model):
            field1 = models.IntegerField(null=True, editable=False)
            field2 = models.IntegerField()
            field3 = models.IntegerField()
            field4 = models.IntegerField()
            field5 = models.IntegerField()

        self.assertRaises(AttributeError, supplemental_fields._check_supplemental_field_attrs, BadModel3())

        class GoodModel(models.Model):
            field1 = models.IntegerField(null=True, blank=False)
            field2 = models.IntegerField(null=True, editable=True)
            field3 = models.IntegerField(null=True)
            field4 = models.IntegerField(null=True)
            field5 = models.IntegerField(null=True)

        self.assertTrue(supplemental_fields._check_supplemental_field_attrs(GoodModel()))

    def test_set_original_model_admin_fields(self):

        class GoodModel(models.Model):
            field1 = models.IntegerField(null=True)
            field2 = models.IntegerField(null=True)
            field3 = models.IntegerField(null=True)
            field4 = models.IntegerField(null=True)
            field5 = models.IntegerField(null=True)
        # try with a tuple
        fields = ('field1', 'field2', 'field3')
        original_fields = [fld.name for fld in GoodModel._meta.fields]
        supplemental_fields = SupplementalFields(fields, 0.231)
        supplemental_fields._set_model_inst(GoodModel())
        self.assertIsNone(supplemental_fields._set_original_model_admin_fields(original_fields))
        self.assertEqual(original_fields, supplemental_fields._get_original_model_admin_fields())
        # change var and confirm does not change instance attribute
        original_fields = ('field1', 'field2', 'field3', 'field4', 'field5', 'erik')
        self.assertNotEqual(original_fields, supplemental_fields._get_original_model_admin_fields())
        # try with a list
        original_fields = ['field1', 'field2', 'field3', 'field4', 'field5']
        supplemental_fields = SupplementalFields(fields, 0.231)
        supplemental_fields._set_original_model_admin_fields(original_fields)
        self.assertEqual(original_fields, supplemental_fields._get_original_model_admin_fields())
        # change var and confirm does not change instance attribute
        original_fields.append('erik')
        self.assertNotEqual(original_fields, supplemental_fields._get_original_model_admin_fields())

    def test_choose_fields_to_exclude(self):
        # p=1, should return an empty list
        supplemental_field_tuple = ('field1', 'field2', 'field3')
        supplemental_fields = SupplementalFields(supplemental_field_tuple, 1.0)
        self.assertEqual(supplemental_fields._choose_fields_to_exclude(), [])
        # p less than 1, should return either an empty list or the list of supplemental fields
        supplemental_fields = SupplementalFields(supplemental_field_tuple, 0.1)
        choice = []
        for i in range(0, 50):
            # call a number of times, should get both eventually
            choice.append(supplemental_fields._choose_fields_to_exclude())
        # we are not testing that the probability is correct, just that
        # given a p<1, should get both possible return values
        self.assertIn(supplemental_field_tuple, choice)
        self.assertIn([], choice)

#     def test_p1(self):
#         sf = SupplementalFields(('f3', 'f4'), p=0.1)
#         seq = sf._get_probability_as_sequence()
#         self.assertEqual(len(seq), 1000)
#         self.assertEqual(seq.count(0), 100)
#         self.assertEqual(seq.count(1), 900)
#  
#         sf = SupplementalFields(('f3', 'f4'), p=0.5)
#         seq = sf._get_probability_as_sequence()
#         self.assertEqual(len(seq), 1000)
#         self.assertEqual(seq.count(0), 500)
#         self.assertEqual(seq.count(1), 500)
#  
#         sf = SupplementalFields(('f3', 'f4'), p=0.135)
#         seq = sf._get_probability_as_sequence()
#         self.assertEqual(len(seq), 1000)
#         self.assertEqual(seq.count(0), 135)
#         self.assertEqual(seq.count(1), 865)
#  
#         self.assertRaises(AttributeError, SupplementalFields, "X", p=0.1)
#         self.assertRaises(AttributeError, SupplementalFields, ('f3', 'f4'), p=1)
#         self.assertRaises(AttributeError, SupplementalFields, ('f3', 'f4'), p=0.1355)
#  
#         P = 0
#         INC = 1
#         EXC = 2
#         for opt in [(0.135, 135, 865), (0.5, 500, 500), (0.75, 750, 250)]:
#             print 'p={0} include(0)={1} exclude(1)={2}'.format(*opt)
#             sf = SupplementalFields(('f3', 'f4'), p=opt[P])
#             self.assertEqual(sf._get_probability_as_sequence().count(0), opt[INC])
#             self.assertEqual(sf._get_probability_as_sequence().count(1), opt[EXC])
#             zero = []
#             one = []
#             for j in range(0, 1000):
#                 lst = []
#                 for i in range(0, 1000):
#                     fields, exclude_fields = sf.choose_fields(('f1', 'f2', 'f3', 'f4', 'f5'), TestModel())
#                     if fields == ('f1', 'f2', 'f3', 'f4', 'f5') and not exclude_fields:
#                         # supp fields were not excluded
#                         lst.append(0)
#                     elif fields == ('f1', 'f2', 'f5') and exclude_fields == ('f3', 'f4'):
#                         # supp fields were excluded
#                         lst.append(1)
#                     else:
#                         lst.append(2)
#                         print '  fields={0}'.format(fields)
#                         print '  exclude_fields={0}'.format(exclude_fields)
#                 zero.append(lst.count(0))
#                 one.append(lst.count(1))
#                 self.assertEqual(lst.count(2), 0)
#                 #if opt[P] > 0.5:
#                 #    self.assertGreater(lst.count(0), lst.count(1))
#                 #elif opt[P] < 0.5:
#                 #    self.assertLess(lst.count(0), lst.count(1))
#                 #else:
#                 #    pass
#                 #print '    0 -> {0} < {1} < {2}'.format(opt[INC] - (opt[INC] * (opt[P] * 2)), lst.count(0), opt[INC] + (opt[INC] * (opt[P] * 2)))
#                 #self.assertTrue(opt[INC] - (opt[INC] * (opt[P] * 2)) < lst.count(0) < opt[INC] + (opt[INC] * (opt[P] * 2)))
#                 #print '    1 -> {0} < {1} < {2}'.format(opt[EXC] - (opt[EXC] * (opt[P] * 2)), lst.count(1), opt[EXC] + (opt[EXC] * (opt[P] * 2)))
#                 #self.assertTrue(opt[EXC] - (opt[EXC] * (opt[P] * 2)) < lst.count(1) < opt[EXC] + (opt[EXC] * (opt[P] * 2)))
#                 #self.assertTrue(lst.count(0) in range(110, 155), lst.count(0))
#                 #self.assertTrue(lst.count(1) in range(850, 883), lst.count(1))
#             print '  Included mean={0} std={1}, n={2}'.format(numpy.mean(zero), numpy.std(zero), len(zero))
#             print '  Excluded mean={0} std={1}, n={2} '.format(numpy.mean(one), numpy.std(one), len(one))

