from ...bhp_base_admin.admin import BaseModelAdmin
from ..actions import encrypt, decrypt


class BaseCryptorModelAdmin (BaseModelAdmin):

    """ Overide ModelAdmin to force username to be saved on add/change and
    other stuff. """

    def __init__(self, *args, **kwargs):
        self.actions.append(encrypt)
        self.actions.append(decrypt)
        super(BaseCryptorModelAdmin, self).__init__(*args, **kwargs)
