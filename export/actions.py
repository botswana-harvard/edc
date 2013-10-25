from edc.export.classes import ExportAsCsv


def export_as_csv_action(description="Export selected objects as CSV file",
                         fields=None, exclude=None, extra_fields=None, header=True):
    """
    Return an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row

    ...in my_app/admin.py add this import:
    from bhp_common.actions import export_as_csv_action

    ...and this to your modeladmin class:
    actions = [export_as_csv_action("CSV Export",
        fields=[],
        exclude=[],
        extra_fields=[],
        )]

    use extra_fields to access field attributes from related models. Pass a
    list of dictionaries [{'label': 'query_string'}, {}, ...]

    """
    def my_getattr(obj, query_list):

        """ Recurse on result of getattr() with a given query string as a list.

                The query_list is based on a django-style query string
                split on '__' into a list.
                For example 'field_attr__model_name__field_attr' split to
                ['field_attr', 'model_name', 'field_attr']
        """

        if len(query_list) > 1:
            try:
                return my_getattr(getattr(obj, query_list[0]), query_list[1:])
            except:
                # DoesNotExist
                return '(none)'
        return getattr(obj, query_list[0])

    def export_as_csv(modeladmin, request, queryset):
        """
        Generic csv export admin action.
        based on http://djangosnippets.org/snippets/1697/

        Added exra_fields and changed accordingly
        """
        exporter = ExportAsCsv(modeladmin, fields, extra_fields)
        return exporter.write_to_csv()

    export_as_csv.short_description = description

    return export_as_csv
