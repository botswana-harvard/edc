from django.db import models
from edc_core.bhp_content_type_map.models import ContentTypeMap
from edc_core.bhp_visit.models import VisitDefinition


class EntryBucketManager(models.Manager):

    def get_by_natural_key(self, visit_definition_code, app_label, model):
        """Returns the instance using the natural key."""
        visit_definition = VisitDefinition.objects.get_by_natural_key(visit_definition_code)
        content_map_type = ContentTypeMap.objects.get_by_natural_key(app_label, model)
        return self.get(content_map_type=content_map_type, visit_definition=visit_definition)
