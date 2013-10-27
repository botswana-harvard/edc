from edc.export.classes import ExportAsCsv


def export_as_csv_action(description="Export selected objects to CSV",
                         fields=None, exclude=None, extra_fields=None, header=True, track_history=True, show_all_fields=True):
    """
    Return an export csv action
    'fields' and 'exclude' work like in django ModelForm
    'header' is whether or not to output the column names as the first row

    in my_app/admin.py add this import::
        from edc.export.actions import export_as_csv_action

    add this to your modeladmin class::
        actions = [export_as_csv_action("CSV Export",
            fields=[],
            exclude=[],
            extra_fields=[],
            )]

    use extra_fields to access field attributes from related models. Pass a
    list of dictionaries [{'label': 'query_string'}, {}, ...]

    """
    def export_as_csv(modeladmin, request, queryset):
        exporter = ExportAsCsv(queryset,
                               modeladmin=modeladmin,
                               fields=fields,
                               exclude=exclude,
                               extra_fields=extra_fields,
                               header=header,
                               track_history=track_history,
                               show_all_fields=show_all_fields)
        return exporter.write_to_file()

    export_as_csv.short_description = description

    return export_as_csv
