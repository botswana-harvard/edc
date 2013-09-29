import factory
from django.contrib.contenttypes.models import ContentType
from edc_core.bhp_base_model.tests.factories import BaseModelFactory


class ContentTypeFactory(BaseModelFactory):
    FACTORY_FOR = ContentType

    name = factory.Sequence(lambda n: 'contenttypemap{0}'.format(n))
    app_label = 'bhp_content_type_map'
    model = factory.Sequence(lambda n: 'contenttypemap{0}'.format(n))
