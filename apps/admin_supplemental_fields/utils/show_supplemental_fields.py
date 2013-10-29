from django.contrib import admin


def show_supplemental_fields(self):
    """Print out admin classes that use supplemental_fields."""
    index = 0
    for value in admin.site._registry.itervalues():
        if 'supplemental_fields' in dir(value):
            index += 1
            print str(index) + '. ' + value.model._meta.object_name
            print '  group: ' + unicode(value.supplemental_fields._group)
            print '  fields: ' + ', '.join(value.supplemental_fields._get_optional_fields())
            print '  probability: ' + unicode(value.supplemental_fields._p)
            print '  db_table: ' + value.model._meta.db_table
