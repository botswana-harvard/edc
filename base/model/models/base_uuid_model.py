from ..fields import UUIDAutoField, RevisionField

from .base_model import BaseModel


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """

    id = UUIDAutoField(
        primary_key=True,
        help_text="system field. uuid primary key."
        )

    revision = RevisionField(
        help_text="system field. Git repository branch:commit."
        )

    class Meta:
        abstract = True
