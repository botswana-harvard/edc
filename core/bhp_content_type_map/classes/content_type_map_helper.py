from django.contrib.contenttypes.models import ContentType
from django.db.models import F
from django.core.exceptions import MultipleObjectsReturned

from ..exceptions import ContentTypeMapError
from ..models import ContentTypeMap


class ContentTypeMapHelper(object):

    def __init__(self, using=None):
        self.using = using or 'default'

    def populate(self):
        """Populates ContentTypeMap with django's ContentTypecontent information."""
        content_types = ContentType.objects.using(self.using).all()
        for content_type in content_types:
            create = True
            try:
                ContentTypeMap.objects.get(content_type=content_type)
                create = False
            except ContentTypeMap.DoesNotExist:
                pass
            except MultipleObjectsReturned:
                ContentTypeMap.objects.filter(content_type=content_type).delete()
            finally:
                if create:
                    verbose_name = content_type.model_class()._meta.verbose_name
                    # print 'Creating ContentTypeMap: {0}'.format(verbose_name)
                    ContentTypeMap.objects.using(self.using).create(
                        content_type=content_type,
                        app_label=content_type.app_label,
                        name=verbose_name,
                        model=content_type.model,
                        module_name=content_type.model)


#             if not self.content_type_map_model_cls.objects.filter(content_type=content_type):
#                 if not self.content_type_map_model_cls.objects.using(self.using).filter(content_type__name=content_type.name).count() == 1:
#                     self.content_type_map_model_cls.objects.using(self.using).filter(content_type__name=content_type.name).delete()
#                 if get_model(content_type.app_label, content_type.model):
#                     verbose_name = get_model(content_type.app_label, content_type.model)._meta.verbose_name
#                 else:
#                     verbose_name = content_type.name
#                 try:
#                     self.content_type_map_model_cls.objects.using(self.using).create(
#                         content_type=content_type,
#                         app_label=content_type.app_label,
#                         name=verbose_name,
#                         model=content_type.model,
#                         module_name=content_type.model)
#                 except:
#                     pass
#        # make sure content_type_map_model_cls has as many records as djangos
#        django_count = ContentType.objects.using(self.using).all().aggregate(Max('id'))
#        bhp_count = self.content_type_map_model_cls.objects.using(self.using).all().aggregate(Max('id'))
#        creation_count = django_count.get('id__max') - bhp_count.get('id__max')
#        if creation_count > 0:
#            for i in range(0, creation_count):
#                self.content_type_map_model_cls.objects.create()

    def sync(self):
        """Syncs content type map foreignkey with django's ContentType id.

        Schema changes might change the key values for records in django's ContentType table.
        Update ContentTypeMap field content_type with the new key."""
        for content_type_map in ContentTypeMap.objects.using(self.using).exclude(name=F('content_type__name')):
            try:
                model = content_type_map.model_class()
                try:
                    content_type = ContentType.objects.using(self.using).get(app_label=model._meta.app_label,
                                                                             model=model._meta.module_name)
                    content_type_map.content_type = content_type
                    content_type_map.save(update_fields=['content_type'])
                except ContentType.DoesNotExist:
                    pass
            except ContentTypeMapError:
                print 'Deleting stale ContentTypeMap {} {}'.format(content_type_map.app_label, content_type_map.model)
                content_type_map.delete()
