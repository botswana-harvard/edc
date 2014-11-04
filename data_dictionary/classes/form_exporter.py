from collections import OrderedDict

from django.contrib import admin
from django.core.exceptions import FieldError
from django.db.models import get_app, get_models, get_model

from edc.base.model.fields.helpers.revision import site_revision
from edc.subject.visit_schedule.models import VisitDefinition
from edc.subject.entry.models import Entry, LabEntry
from edc.subject.rule_groups.classes import site_rule_groups


class FormExporter(object):
    """Exports a model into text format for review as a wiki page or PDF."""
    def __init__(self):
        self._model = None
        self._model_admin = None
        self._model_fields = None
        admin.autodiscover()
        site_rule_groups.autodiscover()

    @property
    def model(self):
        return self._model

    @model.setter
    def model(self, model_cls):
        self._model_admin = None
        self._model_fields = None
        self._model = model_cls

    @property
    def model_admin(self):
        """Finds and returns the model_admin class for the given model."""
        if not self._model_admin:
            for model_admin in admin.sites.site._registry.itervalues():
                if model_admin.model == self.model:
                    self._model_admin = model_admin
                    break
        return self._model_admin

    @property
    def model_fields(self):
        """Returns the field classes from the model listed in model_admin.fields tuple."""
        if not self._model_fields:
            n = 0
            self._model_fields = OrderedDict()
            fields = {field.name: field for field in self.model._meta.fields}
            try:
                for field_name in self.model_admin.fields:
                    n += 1
                    try:
                        field = fields[field_name]
                    except KeyError:
                        try:
                            # m2m?
                            field = getattr(self._model, field_name).field
                        except AttributeError:
                            field = object()
                    field.number = n
                    self._model_fields.update({field_name: field})
            except TypeError:
                pass
            except AttributeError:
                pass
        return self._model_fields

    def question(self, name):
        question = self.model_fields.get(name)
        try:
            for choice in question.choices:
                print choice[1]
        except AttributeError:
            print '___________'
        print 'Simple Errors:'
        for a, b in question.error_messages.iteritems():
            print a, unicode(b)
        print unicode(question)

    @property
    def form(self):
        template = []
        template.append('===={}===='.format(self.model._meta.verbose_name))
        template.append('<small>Edc Docstring: {}</small>\n'.format(self.model.__doc__.replace('\n', '')))
        try:
            if self.model_admin.instructions:
                template.append('<p><B>Instructions: </B>{}</p>'.format(''.join(self.model_admin.instructions)))
        except AttributeError:
            pass
        for attr_name, field in self.model_fields.iteritems():
            template.append('{bold}{}. {}{bold}'.format(
                field.number, unicode(field.verbose_name), bold='\'\'\'' if not field.null else ''))
            choices = ''
            extra = ''
            for choice in field.choices:
                choices += '* {}\n'.format(unicode(choice[1]))
            try:
                # if m2m, try to get to the list model to populate choices
                list_model = getattr(self.model, field.name).field.related.parent_model
                for obj in list_model.objects.all().order_by('display_index'):
                    choices += '* {}\n'.format(unicode(obj.name))
                    # choices += '* {}\n'.
                extra = 'select multiple options'
            except AttributeError:
                pass
            except FieldError:
                pass
            template.append(':<small>{}.{} {}</small>'.format(self.model._meta.db_table, field.name, extra))
            if choices:
                template.append(choices)
            else:
                try:
                    template.append('* dropdown [{}]'.format(field.rel.to._meta.object_name))
                except AttributeError:
                    template.append(': ___________')
            if field.help_text:
                template.append('\'\'{}\'\'\n'.format(unicode(field.help_text)))
        if self.interform_logic:
            template.append('=====Interform rules (Rule Groups)=====')
            template.append(self.interform_logic)
        template.append('<small>Exported from Edc. Revision tag: {}</small>'.format(site_revision.tag))
        template.append('<hr>')
        return template

    def requisition(self, panel_name):
        return ['===={}===='.format(panel_name)]

    def export_by_visit(self, code):
        forms = []
        visit_definition = VisitDefinition.objects.get(code=code)
        print '==={0.code}: {0.title}==='.format(visit_definition)
        for entry in Entry.objects.filter(visit_definition=visit_definition).order_by('entry_order'):
            self.model = entry.content_type_map.model_class()
            forms.append(self.form)
        for lab_entry in LabEntry.objects.filter(visit_definition=visit_definition).order_by('entry_order'):
            forms.append(self.requisition(lab_entry.requisition_panel.name))
        return forms

    def export_by_app(self, app_label):
        forms = []
        app = get_app(app_label)
        models = get_models(app)
        print '===Forms for {}==='.format(app_label)
        for model in models:
            if 'Audit' not in model._meta.object_name:
                self.model = model
                forms.append(self.form)
        return forms

    def export_by_model(self, app_label, model_name):
        forms = []
        self.model = get_model(app_label, model_name)
        forms.append(self.form)
        return forms

    @property
    def interform_logic(self):
        docstring = []
        for rule in site_rule_groups.get_rules_for_source_model(self.model, self.model._meta.app_label):
            docstring.append('#{}\n#*{}'.format(rule, rule.logic.__doc__).format(
                target_model='\'{}\''.format('\'\' and \'\''.join(self.target_model_list(rule)))))
        return '\n'.join(docstring)

    def target_model_list(self, rule):
        target_model_list = []
        for model in rule.target_model_list:
            try:
                target_model_list.append(model._meta.verbose_name)
            except (AttributeError, TypeError):
                target_model_list.append(str(model))
        return target_model_list
