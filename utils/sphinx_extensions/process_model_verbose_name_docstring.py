# http://djangosnippets.org/snippets/2533/
import inspect


def process_model_verbose_name_docstring(app, what, name, obj, options, lines):
    # This causes import errors if left outside the function
    from django.db import models

    # Only look at objects that inherit from Django's base model class
    if inspect.isclass(obj) and issubclass(obj, models.Model):
        if obj._meta.verbose_name[:4].lower() != 'base' and obj._meta.verbose_name[:4].lower() != 'my':
            lines.append(u':Name: %s' % (obj._meta.verbose_name,))
            lines.append(u':Table: %s' % (obj._meta.db_table,))
    return lines
