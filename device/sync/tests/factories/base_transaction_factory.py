from datetime import datetime
from edc.base.model.tests.factories import BaseUuidModelFactory
from ...models import BaseTransaction


class BaseTransactionFactory(BaseUuidModelFactory):
    FACTORY_FOR = BaseTransaction

    tx = 'enc1:::4174e18097cdea4f2d12f510bce513b1fd6ecc70694b26ac75b5e0aa8ace3e06enc2:::SVb5n30wSvOS6nWWm2EuV3Bzh8yjTtT/tSfULFb4F9aH8VkUcbCKwPIDyzjejWc2TstldAcJhIeChxcftuWr1PA4cOiafiZUSP/NYT+SqHxYafH2+ryBBgVzzR3/EQAcfSK3wRQmY+A3ld7u4ExpED9yNeYhiz8eBAbJmxd3Aoym84XGDzXSu3fo30ruIhboCpuNYCqTbqEYSiJtBY9t5c1PLRgxtOve8mBgpMNBsihfEoVQcGeTmjC/Pq7HJFowmS1U/QbiD3kF9HjkfcIcwuW0HZTSaYFBRdwbnpvK8eDaeUiuDQL3/kQ3YQXI0WkJ3SOaUyNbWZRKt5Zjo9oSC53V2oqGaJYeQMAbQZ0kTq3uFy6GUW9lAcr5crejnClkhiRiyDu0MBNDDWFaAjD/gdieN2K8eB9Qb6g1OxKU1YKzt38w8xTBZxrubVxxsAqX1KHvX3PyHw7pZt+2ioaQIkpussrX9wYUrzhpp0bCRTPOHSYVVHszvqVlIrYDcJhAjc'
    tx_name = 'SubjectRequisition'
    tx_pk = '03a72ff5-0105-11e3-baec-7cd1c3dc170f'
    producer = 'mpp54-bhp066_survey'
    action = 'I'
    timestamp = '20130809170439931625'
    consumed_datetime = datetime.today()
    is_ignored = False
    is_error = False