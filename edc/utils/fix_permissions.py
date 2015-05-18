from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType
from django.db.models import get_app, get_models


def fix_permissions(self, app_name):

    app = get_app(app_name)
    for model in get_models(app):
        content_type = ContentType.objects.get_for_model(model)
        for permission in Permission.objects.filter(codename__icontains=content_type.model):
            permission.content_type = content_type
            permission.save()
