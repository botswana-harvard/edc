import socket

from django_extensions.db.fields import UUIDField
from django.db.models import CharField
from django.utils.translation import ugettext as _

from ..helpers.revision import site_revision


class UUIDAutoField (UUIDField):
    """
    This is not technically an AutoField as the DB does not provide the value. A django AutoField
    lets the DB provide the value in base.py (save_base). To avoid that happening here, this
    field inherits from UUIDField->CharField->Field instead of AutoField->Field.

    """
    description = _("UuidAutoField")

    def __init__(self, *args, **kwargs):
        assert kwargs.get('primary_key', False) is True, "%ss must have primary_key=True." % self.__class__.__name__
        UUIDField.__init__(self, *args, **kwargs)

#     def contribute_to_class(self, cls, name):
#         assert not cls._meta.has_auto_field, \
#                "A model can't have more than one AutoField."
#         super(UUIDAutoField, self).contribute_to_class(cls, name)
#         cls._meta.has_auto_field = True
#         cls._meta.auto_field = self


class RevisionField (CharField):
    """Updates the value to the current git branch and commit."""

    description = _("RevisionField")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('null', True)
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('verbose_name', 'Revision')
        CharField.__init__(self, *args, **kwargs)

    def pre_save(self, model, add):
        value = self.get_revision()
        setattr(model, self.attname, value)
        return value

    def get_revision(self):
        return site_revision.get_revision()

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class HostnameCreationField (CharField):
    """
    HostnameCreationField

    By default, sets editable=False, blank=True, default=socket.gethostname()
    """

    description = _("Custom field for hostname created")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('verbose_name', 'Hostname')
        kwargs.setdefault('default', socket.gethostname())
        CharField.__init__(self, *args, **kwargs)

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)


class HostnameModificationField (CharField):
    """
    HostnameModificationField

    By default, sets editable=False, blank=True, default=socket.gethostname()

    Sets value to socket.gethostname() on each save of the model.
    """
    description = _("Custom field for hostname modified")

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('editable', False)
        kwargs.setdefault('blank', True)
        kwargs.setdefault('max_length', 50)
        kwargs.setdefault('verbose_name', 'Hostname')
        kwargs.setdefault('default', socket.gethostname())
        CharField.__init__(self, *args, **kwargs)

    def pre_save(self, model, add):
        value = socket.gethostname()
        setattr(model, self.attname, value)
        return value

    def get_internal_type(self):
        return "CharField"

    def south_field_triple(self):
        "Returns a suitable description of this field for South."
        # We'll just introspect ourselves, since we inherit.
        from south.modelsinspector import introspector
        field_class = "django.db.models.fields.CharField"
        args, kwargs = introspector(self)
        return (field_class, args, kwargs)
