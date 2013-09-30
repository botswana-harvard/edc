from edc.base.admin.admin import BaseTabularInline


class BaseConsentUpdateInlineAdmin(BaseTabularInline):
    extra = 0
    readonly_fields = ('consent_version', )
