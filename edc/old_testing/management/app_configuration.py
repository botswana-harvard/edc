from django.db.models.signals import post_syncdb

import edc.testing.models

from ..classes import TestAppConfiguration


def app_configuration_callback(sender, **kwargs):
    # Your specific logic here
    print 'Loading app configuration'
    TestAppConfiguration().prepare()
    print 'Done. app configuration loaded'

post_syncdb.connect(app_configuration_callback, sender=edc.testing.models)
