from __future__ import print_function

from django.db.models import get_models, get_model, get_app


def generate_review_models(full_app_name):

    app_name = full_app_name.split('.')[-1:][0]
    app = get_app(app_name)
    models = get_models(app)
    print("from {full_app_name}.models import ({model_classes})".format(full_app_name=full_app_name, model_classes=', '.join([model._meta.object_name for model in models if 'Audit' not in model._meta.object_name and not model._meta.proxy])))
    print("")
    print("")
    for model in models:
        if 'Audit' not in model._meta.object_name and not model._meta.proxy:
            print("""
class {model_name}Review({model_name}):

    def save(self, *args, **kwargs):
        pass

    class Meta:
        app_label = '{app_name}'
        proxy = True
""".format(model_name=model._meta.object_name, app_name=app_name))


def generate_review_modeladmin(full_app_name):

    app_name = full_app_name.split('.')[-1:][0]
    app = get_app(app_name)
    models = get_models(app)
    print("from django.contrib import admin")
    print("from .subject_visit_model_admin import SubjectVisitModelAdmin")
    print("from {full_app_name}.models import ({model_classes})".format(full_app_name=full_app_name, model_classes=', '.join([model._meta.object_name for model in models if 'Audit' not in model._meta.object_name and model._meta.proxy])))
    print("")
    print("")
    for model in models:
        if 'Audit' not in model._meta.object_name:
            if 'Audit' not in model._meta.object_name and model._meta.proxy:
                print("""
class {model_name}Admin(SubjectVisitModelAdmin):
    def __init__(self, *args, **kwargs):
        super({model_name}Admin, self).__init__(*args, **kwargs)
        self.readonly_fields = [field.name for field in {model_name}._meta.fields]

admin.site.register({model_name}, {model_name}Admin)
""".format(model_name=model._meta.object_name))
