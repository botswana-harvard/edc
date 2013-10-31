from django.contrib.auth.models import Group, Permission


class Permissions(object):

    def __init__(self, visit_definition_codes, group_name, permission_profile):
        """Add permissions to a group for the models in a visit_definition or list of visit_definitions."""
        # TODO: could add a "view" permission here in addition to django's add, change, delete
        #       maybe use it to manpulate the submit row on the change_form.
        self.set_visit_definitions(visit_definition_codes)
        self.set_permission_profile(permission_profile)
        self.set_group(group_name)
        self.set_content_types(visit_definition_codes)

    def update(self):
        """Updates permissions to the group based on the list of content_types and the profile.

        Permission instance must already exist in the Permissions model (e.g. put in by django on syncdb...)"""
        for content_type in self.get_content_types():
            if 'add' in self.get_permission_profile():
                if not self.get_group().permissions.filter(content_type=content_type, codename__icontains='add' + '_'):
                    self.get_group().permissions.add(Permission.objects.get(content_type=content_type, codename__icontains='add' + '_'))
            if 'change' in self.get_permission_profile():
                if not self.get_group().permissions.filter(content_type=content_type, codename__icontains='change' + '_'):
                    self.get_group().permissions.add(Permission.objects.get(content_type=content_type, codename__icontains='change' + '_'))
            if 'delete' in self.get_permission_profile():
                if not self.get_group().permissions.filter(content_type=content_type, codename__icontains='delete' + '_'):
                    self.get_group().permissions.add(Permission.objects.get(content_type=content_type, codename__icontains='delete' + '_'))

    def replace(self):
        """Replaces permissions to the group by deleting all for this group then calling update."""
        self.clear_permissions_for_group()
        self.update()

    def clear_permissions_for_group(self):
        """"Clears permissions for this group."""
        self.get_group().permissions.all().delete()

    def set_group(self, group_name):
        """Sets to the group and creates if the group does not exist."""
        if not Group.objects.filter(name=group_name):
            Group.objects.create(name=group_name)
        self._group = Group.objects.get(name=group_name)

    def get_group(self):
        return self._group

    def set_permission_profile(self, value_list):
        self._permission_profile = value_list
        if not value_list:
            self._permission_profile = ['add', 'change']

    def get_permission_profile(self):
        return self._permission_profile

    def set_visit_definitions(self, codes):
        from ..models import VisitDefinition
        self._visit_definitions = VisitDefinition.objects.filter(code__in=codes)
        if not self._visit_definitions:
            raise AttributeError('Attribute visit_definitions cannot be None. Could not find any matching codes in {0}'.format(codes))

    def get_visit_definitions(self):
        return self._visit_definitions

    def set_content_types(self, codes):
        """Sets to a complete and unique list of content types from each Entry in the visit definition."""
        from edc.subject.entry.models import Entry

        self._content_types = []
        for visit_definition in self.get_visit_definitions():
            for entry in Entry.objects.filter(visit_definition=visit_definition):
                if entry.content_type_map.content_type not in self._content_types:
                    self._content_types.append(entry.content_type_map.content_type)

    def get_content_types(self):
        return self._content_types
