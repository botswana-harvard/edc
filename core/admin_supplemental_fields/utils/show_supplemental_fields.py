from django.contrib import admin


def show_supplemental_fields(self):
    index = 0
    for value in admin.site._registry.itervalues():
        if 'supplemental_fields' in dir(value):
            index += 1
            print str(index) + '. *************************'
            print 'form: ' + value.model._meta.object_name
            print 'category' + unicode(value.supplemental_fields._group)
            print 'probability: ' + unicode(value.supplemental_fields._p)
            print 'db_table: ' + value.model._meta.db_table
