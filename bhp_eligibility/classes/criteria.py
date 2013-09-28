from datetime import timedelta
from django.db.models import Q, get_model
from bhp_eligibility.models import Criteria as CriteriaModel


class Criteria(object):

    def __init__(self):
        self.error = None
        self.valid_criteria = []

    def validate_labs(self, subject_identifier, reference_datetime, model_name, criteria):
        """Validate lab criteria.

        Args:
            subject_identifier:
            reference_datetime: for timedelta calc of days item in criteria tuple
            model_name: eligibility model that is calling this method
            criteria: tuples in a tuple of format ((test_code, operator, value, days), (), ...)
                      where test_code is a list, operator is gt, gte, lt, lte, etc and days is a pos/neg integer.
        """
        # TODO: might be better to refer to the lab_clinic_api panel name instead of the test_code??
        ResultItem = get_model('lab_clinic_api', 'resultitem')

        TEST_CODE = 0
        OPERATOR = 1
        VALUE = 2
        UNITS = 3
        DAYS = 4
        self.valid_criteria = []
        self.error = None
        for item in criteria:
            dte = reference_datetime - timedelta(days=item[DAYS])
            qset = Q()
            qset.add(Q(test_code__code__in=item[TEST_CODE]), Q.AND)
            qset.add(Q(result__order__aliquot__receive__drawn_datetime__gt=dte), Q.AND)
            qset.add(Q(result__subject_identifier=subject_identifier), Q.AND)
            qset.add(Q(test_code__units=item[UNITS]), Q.AND)
            if ResultItem.objects.filter(qset, **{'result_item_value_as_float__{0}'.format(item[OPERATOR]): item[VALUE]}).exists():
                result_item = ResultItem.objects.filter(qset)
                for r in result_item:
                    self.valid_criteria.append(
                        '({test_code} on {result_datetime} = {result_value}. '
                        'This is \'{operator}\' {value} {units} within {days} of {reference_datetime}.)'.format(
                        test_code=r.test_code,
                        result_datetime=r.result.order.aliquot.receive.drawn_datetime,
                        result_value=r.result_item_value_as_float,
                        operator=item[OPERATOR],
                        value=item[VALUE],
                        units=item[UNITS],
                        days=item[DAYS],
                        reference_datetime=reference_datetime))
            else:
                self.valid_criteria = []
                self.error = item
                break
        if self.valid_criteria:
            retval = True
            for criteria in self.valid_criteria:
                # add to criteria model
                # TODO: should existing criteria be overwritten (get_or_create)?
                CriteriaModel.objects.create(
                    subject_identifier=subject_identifier,
                    reference_datetime=reference_datetime,
                    model_name=model_name,
                    criteria=criteria)
        else:
            retval = False
        return retval
