from django.contrib import admin


def show_supplemental_fields():
    """Print out admin classes that use supplemental_fields."""
    admin.autodiscover()
    dct = {}
    for value in admin.site._registry.itervalues():
        if 'supplemental_fields' in dir(value):
            dct.update({value.supplemental_fields.get_group(): []})
    for value in admin.site._registry.itervalues():
        if 'supplemental_fields' in dir(value):
            description = [value.model._meta.object_name,
                           '  group: ' + unicode(value.supplemental_fields.get_group()),
                           '  grouping: ' + unicode(value.supplemental_fields.get_grouping_field()),
                           '  fields: ' + ', '.join(value.supplemental_fields.get_supplemental_fields()),
                           '  probability: ' + unicode(value.supplemental_fields.get_probability()),
                           '  db_table: ' + value.model._meta.db_table]
            dct[value.supplemental_fields.get_group()].append({value.model._meta.object_name: description})
    for description in dct.itervalues():
        for dct in description:
            for value in dct.itervalues():
                for line in value:
                    print line
