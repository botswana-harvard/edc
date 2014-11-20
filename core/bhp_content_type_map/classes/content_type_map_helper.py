from django.contrib.contenttypes.models import ContentType
from django.core.exceptions import MultipleObjectsReturned
from django.db.models import F


from ..exceptions import ContentTypeMapError
from ..models import ContentTypeMap


class ContentTypeMapHelper(object):

    def __init__(self, using=None):
        self.using = using or 'default'

    def populate(self):
        """Populates ContentTypeMap with django's ContentType information."""
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
            except AttributeError:
                ContentTypeMap.objects.filter(content_type=content_type).delete()
            finally:
                if create:
                    try:
                        ContentTypeMap.objects.using(self.using).create(
                            content_type=content_type,
                            app_label=content_type.app_label,
                            name=content_type.model_class()._meta.verbose_name,
                            model=content_type.model,
                            module_name=content_type.model_class()._meta.module_name)
                    except AttributeError as attribute_error:
                        if 'object has no attribute \'_meta\'' in str(attribute_error):
                            pass

    def sync(self):
        """Syncs content type map foreignkey with django's ContentType id.

        Schema changes might change the key values for records in django's ContentType table.
        Update ContentTypeMap field content_type with the new key."""
        for content_type_map in ContentTypeMap.objects.using(self.using).exclude(name=F('content_type__name')):
            try:
                model = content_type_map.model_class()
                try:
                    content_type = ContentType.objects.using(self.using).get(
                        app_label=model._meta.app_label, model=model._meta.object_name.lower())
                    content_type_map.content_type = content_type
                    content_type_map.save(update_fields=['content_type'])
                except ContentType.DoesNotExist:
                    pass
            except ContentTypeMapError as err_message:
                print 'Deleting stale ContentTypeMap {}.{}. Got {}'.format(
                    content_type_map.app_label, content_type_map.model, err_message)
                content_type_map.delete()
