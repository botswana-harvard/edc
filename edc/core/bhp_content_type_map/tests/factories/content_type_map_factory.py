import factory

from edc.core.bhp_content_type_map.models import ContentTypeMap

from .content_type_factory import ContentTypeFactory


class ContentTypeMapFactory(factory.django.DjangoModelFactory):

    class Meta:
        model = ContentTypeMap

    content_type = factory.SubFactory(ContentTypeFactory)
    name = factory.LazyAttribute(lambda o: '{0}'.format(o.content_type.model_class()._meta.verbose_name))
    app_label = factory.LazyAttribute(lambda o: '{0}'.format(o.content_type.model_class()._meta.app_label))
    model = factory.LazyAttribute(lambda o: '{0}'.format(o.content_type.model_class()._meta.object_name))
