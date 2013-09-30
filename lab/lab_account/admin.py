from django.contrib import admin
from edc.core.bhp_base_admin.admin import BaseModelAdmin
from edc.lab.lab_account.models import Account


class AccountAdmin(BaseModelAdmin):
    list_per_page = 15
admin.site.register(Account, AccountAdmin)
