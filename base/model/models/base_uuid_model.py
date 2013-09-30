from ..fields import MyUUIDField
from .base_model import BaseModel


class BaseUuidModel(BaseModel):

    """Base model class for all models using an UUID and not an INT for the primary key. """

    id = MyUUIDField(primary_key=True)

    class Meta:
        abstract = True
