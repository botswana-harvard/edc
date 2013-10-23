from ..fields import UUIDAutoField, RevisionField

from .base_model import BaseModel


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """

    id = UUIDAutoField(primary_key=True)

    revision = RevisionField()

    class Meta:
        abstract = True
