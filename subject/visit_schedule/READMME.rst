


visit_definition = VisitDefinition.objects.get(code='T0')
content_type_map = ContentTypeMap.objects.get(model='subjectreferral')
Entry.objects.create(visit_definition=visit_definition, entry_order=360, content_type_map=content_type_map)