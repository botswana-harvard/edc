# from django.db.models.signals import post_syncdb

from ..classes import TestAppConfiguration

# from edc.testing import models


def app_configuration_callback(sender, **kwargs):
    # Your specific logic here
    print 'Loading app configuration'
    TestAppConfiguration()
    print 'app configuration loaded'

# post_syncdb.connect(app_configuration_callback, sender=models)
