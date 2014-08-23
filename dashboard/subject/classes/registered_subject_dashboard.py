import re

from textwrap import wrap

from django.core.exceptions import ImproperlyConfigured
from django.core.urlresolvers import reverse
from django.db import models
from django.db.models import TextField, Count
from django.template.loader import render_to_string

from edc.apps.app_configuration.models.global_configuration import GlobalConfiguration
from edc.constants import NEW, NOT_REQUIRED
from edc.core.bhp_common.utils import convert_from_camel
from edc.core.bhp_data_manager.models import ActionItem
from edc.core.crypto_fields.fields import EncryptedTextField
from edc.dashboard.base.classes import Dashboard
from edc.entry_meta_data.helpers import ScheduledEntryMetaDataHelper, RequisitionMetaDataHelper
from edc.lab.lab_clinic_api.classes import EdcLabResults
from edc.lab.lab_packing.models import BasePackingList
from edc.lab.lab_requisition.models import BaseBaseRequisition
from edc.subject.appointment.constants import IN_PROGRESS
from edc.subject.appointment.models import Appointment
from edc.subject.lab_tracker.classes import site_lab_tracker
from edc.subject.locator.models import BaseLocator
from edc.subject.registration.models import RegisteredSubject
from edc.subject.subject_config.models import SubjectConfiguration
from edc.subject.subject_summary.models import Link
from edc.subject.visit_schedule.classes import MembershipFormHelper
from edc.subject.visit_schedule.exceptions import MembershipFormError
from edc.subject.visit_schedule.models import MembershipForm
from edc.subject.visit_tracking.models import BaseVisitTracking
from edc.core.bhp_data_manager.models import TimePointCompletion
from edc.utils.collections import flatten

from .scheduled_entry_context import ScheduledEntryContext
from .requisition_context import RequisitionContext


class RegisteredSubjectDashboard(Dashboard):

    view = None
    dashboard_url_name = 'subject_dashboard_url'

    def __init__(self, dashboard_type, dashboard_id, dashboard_model, dashboard_type_list=None, dashboard_models=None,
                 membership_form_category=None, visit_model=None, registered_subject=None, show=None, **kwargs):

        self._appointment = None
        self._appointment_zero = None
        self._appointment_code = None
        self._appointment_continuation_count = None

        dashboard_models = dashboard_models or {}
        dashboard_models.update({'appointment': Appointment})
        if visit_model:  # usually None, except in testing, usually proved by the subclass. needed now regardless since passing method for one of the dashboard models below
            self.visit_model = visit_model
        dashboard_models.update({'visit': self.visit_model})

        super(RegisteredSubjectDashboard, self).__init__(dashboard_type, dashboard_id, dashboard_model, dashboard_type_list, dashboard_models)

        self.appointment_row_template = 'appointment_row.html'
        self.visit_messages = []
        self.exclude_others_if_keyed_model_name = ''
        self.is_dispatched, self.dispatch_producer = False, None
        self.has_requisition_model = True

        self.registered_subject = registered_subject
        self.membership_form_category = membership_form_category
        self.show = show
        self.set_has_requisition_model = kwargs.get('has_requisition_model')
        if visit_model:
            self.visit_model = visit_model
        if kwargs.get('requisition_model'):
            self.requisition_model = kwargs.get('requisition_model')

    def add_to_context(self):
        self.context.add(
            IN_PROGRESS=IN_PROGRESS,
            NEW=NEW,
            NOT_REQUIRED=NOT_REQUIRED,
            appointment=self.appointment,
            appointment_meta=Appointment._meta,
            appointment_row_template=self.appointment_row_template,
            appointment_visit_attr=self.visit_model._meta.object_name.lower(),
            appointments=self.appointments,
            extra_url_context=self.extra_url_context,
            form_language_code=self.language,
            keyed_membership_forms=self.keyed_subject_membership_models,
            membership_forms=self.subject_membership_models,
            registered_subject=self.registered_subject,
            show=self.show,
            subject_configuration=self.subject_configuration,
            subject_configuration_meta=SubjectConfiguration._meta,
            subject_dashboard_url=self.dashboard_url_name,
            subject_hiv_history=self.subject_hiv_history,
            subject_hiv_status=self.render_subject_hiv_status(),
            subject_identifier=self.subject_identifier,
            unkeyed_membership_forms=self.unkeyed_subject_membership_models,
            visit_attr=convert_from_camel(self.visit_model._meta.object_name),
            visit_code=self.appointment_code,
            visit_instance=self.appointment_continuation_count,
            visit_messages=self.visit_messages,
            visit_model=self.visit_model,
            visit_model_instance=self.visit_model_instance,
            visit_model_meta=self.visit_model._meta,
            time_point_completion=self.time_point_completion,
            time_point_completion_meta=TimePointCompletion._meta,
            )
        if self.show == 'forms':
            self.context.add(
                requisition_model=self.requisition_model,
                rendered_scheduled_forms=self.render_scheduled_forms(),
                )
            if self.requisition_model:
                self.context.add(requisition_model_meta=self.requisition_model._meta)
                self.context.add(rendered_scheduled_requisitions=self.render_requisitions())
            self.render_summary_links()
        self.context.add(rendered_action_items=self.render_action_item())
        self.context.add(rendered_locator=self.render_locator())
        self.context.add(self.lab_results_data())

    @classmethod
    def add_to_urlpattern_string(cls):
        return '(?P<show>{show})/'

    @classmethod
    def add_to_urlpattern_string_kwargs(cls):
        return {'show': 'appointments|forms'}

    @property
    def home_url(self):
        """Returns a home url."""
        return reverse(
            self.dashboard_url_name,
            kwargs={'dashboard_type': self.dashboard_type,
                    'dashboard_model': self.dashboard_model_name,
                    'dashboard_id': self.dashboard_id,
                    'show': 'forms'})

    def verify_dashboard_model(self, value):
        """Verify the dashboard model has a way to get to registered_subject."""
        for model in value.itervalues():
            if model:
                if not 'get_registered_subject' in dir(model):
                    raise ImproperlyConfigured('RegisteredSubjectDashboard dashboard_model {0} must have method registered_subject. See {1}.'.format(model, self))

    def add_visit_message(self, message):
        self.visit_messages.append(message)

    @property
    def consent(self):
        return None

    @property
    def subject_hiv_status(self):
        """Returns to the value returned by the site_lab_tracker for this registered subject."""
        self._subject_hiv_status = None
        if self.registered_subject:
            self._subject_hiv_status = site_lab_tracker.get_current_value('HIV', self.registered_subject.subject_identifier, self.registered_subject.subject_type)[0]
        return self._subject_hiv_status

    @property
    def subject_hiv_history(self):
        """Returns to the value returned by the site_lab_tracker for this registered subject."""
        self._subject_hiv_history = None
        if self.registered_subject:
            self._subject_hiv_history = site_lab_tracker.get_history_as_string('HIV', self.registered_subject.subject_identifier, self.registered_subject.subject_type)
        return self._subject_hiv_history

    @property
    def view(self):
        return 'subject_dashbaord'  # TODO: default this for now, but should be removed

    @property
    def registered_subject(self):
        return self._registered_subject

    @registered_subject.setter
    def registered_subject(self, pk=None):
        self._registered_subject = None
        self.set_registered_subject(pk)
        re_pk = re.compile('[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12}')
        if not self._registered_subject:
            if not self._registered_subject and self.dashboard_model == RegisteredSubject:
                self._registered_subject = RegisteredSubject.objects.filter(pk=self.dashboard_id).order_by('-created')[0]
            elif not self._registered_subject and 'get_registered_subject' in dir(self.dashboard_model):
                self._registered_subject = self.dashboard_model_instance.registered_subject
            elif not self._registered_subject and re_pk.match(str(pk)):
                self._registered_subject = RegisteredSubject.objects.get(pk=pk)
            elif not self._registered_subject and self.appointment:
                # can i get it from an appointment? TODO: is this even possible?
                self._registered_subject = self.appointment.registered_subject
            elif self._registered_subject:
                if not isinstance(self._registered_subject, RegisteredSubject):
                    raise TypeError('Expected instance of RegisteredSubject. See {0}'.format(self))
            else:
                pass
        if not self._registered_subject:
            raise TypeError('Attribute \'_registered_subject\' may not be None. Perhaps add method registered_subject to the model {0}. See {1}'.format(self.dashboard_model, self))

    @property
    def appointment(self):
        if not self._appointment:
            if self.dashboard_model_name == 'appointment':
                self._appointment = Appointment.objects.get(pk=self.dashboard_id)
            elif self.dashboard_model_name == 'visit':
                self._appointment = self.visit_model.objects.get(pk=self.dashboard_id).appointment
            else:
                self._appointment = None
            self._appointment_zero = None
            self._appointment_code = None
            self._appointment_continuation_count = None
        return self._appointment

    @property
    def appointment_zero(self):
        if not self._appointment_zero:
            if self.appointment:
                if self.appointment.visit_instance == '0':
                    self._appointment_zero = self.appointment
                else:
                    if Appointment.objects.filter(registered_subject=self.appointment.registered_subject, visit_definition=self.appointment.visit_definition, visit_instance=0) > 1:
                        self.delete_duplicate_appointments(inst=self)
                    self._appointment_zero = Appointment.objects.get(registered_subject=self.appointment.registered_subject, visit_definition=self.appointment.visit_definition, visit_instance=0)
        return self._appointment_zero

    @property
    def appointment_code(self):
        if not self._appointment_code:
            if self.appointment:
                self._appointment_code = self._appointment.visit_definition.code
        return self._appointment_code

    @property
    def appointment_continuation_count(self):
        if not self._appointment_continuation_count:
            if self.appointment:
                self._appointment_continuation_count = self._appointment.visit_instance
        return self._appointment_continuation_count

    @classmethod
    def delete_duplicate_appointments(cls, inst=None, visit_model=None):
        """Deletes all but one duplicate appointments as long as they are not related to a visit model."""
        if not visit_model:
            visit_model = inst.visit_model
        appointments = Appointment.objects.values('registered_subject__pk', 'visit_definition', 'visit_instance').all().annotate(num=Count('pk')).order_by()
        dups = [a for a in appointments if a.get('num') > 1]
        for dup in dups:
            num = dup['num']
            del dup['num']
            for dup_appt in Appointment.objects.filter(**dup):
                if not visit_model.objects.filter(appointment=dup_appt):
                    try:
                        print 'delete {0}'.format(dup_appt)
                        dup_appt.delete()
                        num -= 1
                    except:
                        pass
                    if num == 1:
                        break  # leave one

    @property
    def appointments(self):
        """Returns all appointments for this registered_subject or just one (if given a appointment_code and appointment_continuation_count).

        Could show
            one
            all
            only for this membership form category (which is the subject type)
            only those for a given membership form
            only those for a visit definition grouping
            """
        self._appointments = None
        if self.show == 'forms':
            self._appointments = [self.appointment]
        else:
            # or filter appointments for the current membership categories
            # schedule_group__membership_form
            codes = []
            for category in self.membership_form_category:
                codes.append(MembershipForm.objects.codes_for_category(membership_form_category=category))
                codes = flatten(codes)
                self._appointments = Appointment.objects.filter(
                        registered_subject=self.registered_subject,
                        visit_definition__code__in=codes).order_by('visit_definition__code', 'visit_instance', 'appt_datetime')
        return self._appointments

    @property
    def visit_model(self):
        return self._visit_model

    @visit_model.setter
    def visit_model(self, visit_model):
        self._visit_model = visit_model
        if not self._visit_model:
            raise TypeError('Attribute _visit_model may not be None. Override the method to return a visit mode class or specify at init.')
        if not issubclass(self._visit_model, BaseVisitTracking):
            raise TypeError('Expected visit model class to be a subclass of BaseVisitTracking. Got {0}. See {1}.'.format(self._visit_model, self))

    @property
    def visit_model_attrname(self):
        """Returns what is assumed to be the field name for the visit model in appointment based on the visit model object name."""
        return convert_from_camel(self.visit_model._meta.object_name)

    @property
    def visit_model_rel_attrname(self):
        """Returns what is assumed to be the field name for the visit model in appointment based on the visit model object name."""
        return self.visit_model._meta.object_name.lower()

    @property
    def visit_model_instance(self):
        """Returns the visit model instance but may be None."""
        if self.appointment:
            self._visit_model_instance = self.visit_model.objects.get(appointment=self.appointment)
        elif self.dashboard_model_name == 'visit':
            self._visit_model_instance = self.visit_model.objects.get(pk=self.dashboard_id)
        else:
            self._visit_model_instance = None
        if self._visit_model_instance:
            if not isinstance(self._visit_model_instance, self.visit_model):
                raise TypeError('Expected an instance of visit model class {0}.'.format(self.visit_model))
        return self._visit_model_instance

    @property
    def requisition_model(self):
        return self._requisition_model

    @requisition_model.setter
    def set_requisition_model(self, requisition_model):
        self._requisition_model = requisition_model
        if self.has_requisition_model:
            if not self._requisition_model:
                raise TypeError('Attribute _requisition model cannot be None. See {0}'.format(self))
            if not issubclass(self._requisition_model, BaseBaseRequisition):
                raise TypeError('Expected a subclass of BaseBaseRequisition. Got {0}. See {1}.'.format(self._requisition_model, self))

    @property
    def packing_list_model(self):
        return self._packing_list_model

    @packing_list_model.setter
    def packing_list_model(self):
        self._packing_list_model = self.packing_list_model
        if not self._packing_list_model:
            raise TypeError('Attribute \'_packing_list_model\' may not be None. Override the getter. See {0}'.format(self))
        if not issubclass(self._packing_list_model, BasePackingList):
            raise TypeError('Expected a subclass of BasePackingList. Got {0}. See {1}.'.format(self._packing_list_model, self))

    @property
    def subject_membership_models(self):
        """Sets to a dictionary of membership "models" that are keyed model instances and unkeyed model classes.

        Membership forms can also be proxy models ... see mochudi_subject.models."""
        helper = MembershipFormHelper()
        self._subject_membership_models = []
        for category in self.membership_form_category:
            self._subject_membership_models.append(helper.get_membership_models_for(
                self.registered_subject,
                category,
                extra_grouping_key=self.exclude_others_if_keyed_model_name))
        return self._subject_membership_models

    @property
    def keyed_subject_membership_models(self):
        keyed = []
        for member_model in self.subject_membership_models:
            keyed.append(member_model.get('keyed'))
        keyed = flatten(keyed)
        return keyed

    @property
    def unkeyed_subject_membership_models(self):
        unkeyed = []
        for member_model in self.subject_membership_models:
            unkeyed.append(member_model.get('unkeyed'))
        unkeyed = flatten(unkeyed)
        return unkeyed

    @property
    def membership_form_category(self):
        return self._membership_form_category

    @membership_form_category.setter
    def membership_form_category(self, category):
        """Sets the membership_form_category for this registered subject dashboard needed to filter the QuerySet of Membership forms to display on the dashboard.

        May come from url or from the overridden :func:`set_membership_form_category`

        Must be a valid membership form category."""
        self._membership_form_category=[]
        self._membership_form_category.append(category)
        self._membership_form_category = flatten(self._membership_form_category)
#         self._membership_form_category = category
        for c in self._membership_form_category:
            if c not in self.membership_form_categories:
                raise ImproperlyConfigured('Invalid membership_form category. Attribute \'_membership_form_category\'=\'{0}\' not found in '
                                       'MembershipForms. Must be one of {1}. See {2}.'.format(c, self.membership_form_categories, self))

    @property
    def membership_form_categories(self):
        """Sets to a list of valid categories.

        .. note:: the list of categories is based on those that appear in the MembershipForm category field.
                  The MembershipForm field \'category\' may be a string of category names delimited by a comma."""
        self._membership_form_categories = []
        categories = MembershipForm.objects.values('category').order_by('category').distinct()
        # turn into a list, split and strip
        for c in categories:
            self._membership_form_categories.extend([x.strip() for x in c['category'].split(',')])
        self._membership_form_categories = list(set(self._membership_form_categories))
        if not self._membership_form_categories:
            raise MembershipFormError('Attribute _categories may not be None. Have any membership forms been defined?. See module \'edc.subject.visit_schedule\'. See {0}'.format(self))
        return self._membership_form_categories

    @property
    def subject_type(self):
        return self.registered_subject.subject_type

    @property
    def subject_identifier(self):
        self._subject_identifier = None
        if self.registered_subject:
            self._subject_identifier = self.registered_subject.subject_identifier
        return self._subject_identifier

    @property
    def subject_configuration(self):
        self._subject_configuration = None
        if self.subject_identifier:
            if SubjectConfiguration.objects.filter(subject_identifier=self.subject_identifier):
                self._subject_configuration = SubjectConfiguration.objects.get(subject_identifier=self.subject_identifier)
        return self._subject_configuration

    @property
    def time_point_completion(self):
        self._time_point_completion = None
        if self.registered_subject:
            if TimePointCompletion.objects.filter(registered_subject=self.registered_subject):
                self._time_point_completion = TimePointCompletion.objects.filter(registered_subject=self.registered_subject)[0]
        return self._time_point_completion

    @property
    def show(self):
        return self._show

    @show.setter
    def show(self, value):
        self._show = value or 'appointments'

    def render_summary_links(self, template_filename=None):
        """Renders the side bar template for subject summaries."""
        if not template_filename:
            template_filename = 'summary_side_bar.html'
        summary_links = render_to_string(template_filename, {
                'links': Link.objects.filter(dashboard_type=self.dashboard_type),
                'subject_identifier': self.subject_identifier})
        self.context.add(summary_links=summary_links)

    def render_labs(self):
        """Renders labs for the template side bar if the requisition model is set, by default will not update.

        .. seealso:: :class:`lab_clinic_api.classes.EdcLabResults`"""

        if self._requisition_model:
            edc_lab_results = EdcLabResults()
            return edc_lab_results.render(self.subject_identifier, False)
        return ''

    def lab_results_data(self):
        """Achieves almost the same end result with the render_labs method above but depends on template inclusion"""
        return EdcLabResults().context_data(self.subject_identifier, False) if self._requisition_model else {}

    @property
    def locator_model(self):
        return self._locator_model

    @locator_model.setter
    def locator_model(self, model):
        """Sets the locator model class which must be a subclass of edc.subject.locator.BaseLocator."""
        self._locator_model = model
        if self._locator_model:
            if not issubclass(self._locator_model, BaseLocator):
                raise TypeError('Locator model must be a subclass of BaseLocator. See {0}'.format(self))

    @property
    def locator_inst(self):
        """Sets to a locator model instance for the registered_subject."""
        self._locator_inst = None
        if self.locator_model:
            if self.locator_model.objects.filter(registered_subject=self.locator_registered_subject):
                self._locator_inst = self.locator_model.objects.get(registered_subject=self.locator_registered_subject)
        return self._locator_inst

    @property
    def locator_registered_subject(self):
        """Users may override to return a registered_subject other than the current or None -- used to filter the locator model.

        For example, current subject is an infant, need mother\'s registered subject instance to filter Locator model."""
        return self.registered_subject

    @property
    def locator_visit_model(self):
        """Users may override to return a visit_model other than the current or None -- used to filter the locator model."""
        return self.visit_model

    @property
    def locator_visit_model_attrname(self):
        return convert_from_camel(self.locator_visit_model._meta.object_name)  # ??

    @property
    def locator_scheduled_visit_code(self):
        """ Returns visit where the locator is scheduled, TODO: maybe search visit definition for this?."""
        return None

    @property
    def locator_template(self):
        """Users may override to return a custom locator template."""
        return 'locator_include.html'

    @property
    def subject_hiv_template(self):
        return 'subject_hiv_status.html'

    def render_locator(self):
        """Renders to string the locator for the current locator instance if it is set.

        .. note:: getting access to the correct visit model instance for the locator
                  is a bit tricky. locator model is usually scheduled once for the
                  subject type and otherwise edited from the dashboard sidebar. It may
                  also be 'added' from the dashboard sidebar. Either way, the visit model
                  instance is required -- that being the instance that was (or would
                  have been) used if updated as a scheduled form. If the dashboard is
                  in appointments mode, there is no selected visit model instance.
                  Similarly, if the locator is edited from another dashboard, such as
                  the infant dashboard with maternal/infant pairs, the maternal visit
                  instance is not known. Some methods may be overriden to solve this.
                  They all have 'locator' in the name."""
        context = {}
        if self.locator_model:
            locator_add_url = None
            locator_change_url = None
            if not self.locator_inst:
                context.update({'locator': None})
                locator_add_url = reverse('admin:' + self.locator_model._meta.app_label + '_' + self.locator_model._meta.module_name + '_add')
            if self.locator_inst:
                context.update({'locator': self.locator_inst})
                locator_change_url = reverse('admin:' + self.locator_model._meta.app_label + '_' + self.locator_model._meta.module_name + '_change', args=(self.locator_inst.pk, ))
                for field in self.locator_inst._meta.fields:
                    if isinstance(field, (TextField)):
                        value = getattr(self.locator_inst, field.name)
                        if value:
                            setattr(self.locator_inst, field.name, '<BR>'.join(wrap(value, 25)))
            context.update({
                'subject_dashboard_url': self.dashboard_url_name,
                'dashboard_type': self.dashboard_type,
                'dashboard_model': self.dashboard_model_name,
                'dashboard_id': self.dashboard_id,
                'show': self.show,
                'registered_subject': self.registered_subject,
                'visit_attr': self.visit_model_attrname,
                'visit_model_instance': self.visit_model_instance,
                'appointment': self.appointment,
                'locator_add_url': locator_add_url,
                'locator_change_url': locator_change_url})
        # subclass may insert / update context values (e.g. visit stuff)
            context = self.update_locator_context(context)
        return render_to_string(self.locator_template, context)

    def update_locator_context(self, context):
        """Update context to set visit information if needing something other than the default."""
        if context.get('visit_model_instance'):
            if not isinstance(context.get('visit_model_instance'), self.locator_visit_model):
                context['visit_model_instance'] = None
        if not context.get('visit_model_instance'):
            if self.locator_inst:
                visit_model_instance = getattr(self.locator_inst, self.locator_visit_model_attrname)
            else:
                locator_visit_code = self.locator_scheduled_visit_code
                visit_model_instance = None
                if self.locator_model.objects.filter(registered_subject=self.locator_registered_subject):
                    visit_model_instance = self.locator_model.objects.get(registered_subject=self.locator_registered_subject).maternal_visit
                elif self.locator_visit_model.objects.filter(appointment__registered_subject=self.locator_registered_subject, appointment__visit_definition__code=locator_visit_code, appointment__visit_instance=0):
                    visit_model_instance = self.locator_visit_model.objects.get(appointment__registered_subject=self.locator_registered_subject, appointment__visit_definition__code=locator_visit_code, appointment__visit_instance=0)
                else:
                    pass
            if visit_model_instance:
                context.update({'visit_attr': convert_from_camel(visit_model_instance._meta.object_name), 'visit_model_instance': visit_model_instance})
        return context

    def render_action_item(self, action_item_cls=None, template=None, **kwargs):
        """Renders to string the action_items for the current registered subject."""
        source_registered_subject = kwargs.get('registered_subject', self.registered_subject)
        action_item_cls = action_item_cls or ActionItem
        if isinstance(action_item_cls, models.Model):
            raise TypeError('Expected first parameter to be a Action Item model class. Got an instance. Please correct in local dashboard view.')
        #action_item_add_url = reverse('admin:' + action_item_cls._meta.app_label + '_' + action_item_cls._meta.module_name + '_add')
        if not template:
            template = 'action_item_include.html'
        action_items = action_item_cls.objects.filter(registered_subject=source_registered_subject, display_on_dashboard=True, status='Open')
        action_item_instances = []
        if action_items:
            for action_item in action_items:
                for field in action_item._meta.fields:
                    if isinstance(field, (TextField, EncryptedTextField)):
                        value = getattr(action_item, field.name)
                        if value:
                            setattr(action_item, field.name, '<BR>'.join(wrap(value, 25)))
                action_item_instances.append(action_item)
        if action_item_instances:
            self.context.add(action_item_message='Action items exist for this subject. Please review and resolve if possible.')
        else:
            self.context.add(action_item_message=None)
        rendered_action_items = render_to_string(template, {
            'action_items': action_item_instances,
            'registered_subject': self.registered_subject,
            'dashboard_type': self.dashboard_type,
            'dashboard_model': self.dashboard_model_name,
            'dashboard_id': self.dashboard_id,
            'show': self.show,
            'action_item_meta': action_item_cls._meta})
        return rendered_action_items

    def render_scheduled_forms(self):
        """Renders the Scheduled Entry Forms section of the dashboard using the context class ScheduledEntryContext."""
        template = 'scheduled_entries.html'
        scheduled_entries = []
        scheduled_entry_helper = ScheduledEntryMetaDataHelper(self.appointment_zero, self.visit_model, self.visit_model_attrname)
        for meta_data_instance in scheduled_entry_helper.get_entries_for('clinic'):
            scheduled_entry_context = ScheduledEntryContext(meta_data_instance, self.appointment, self.visit_model)
            scheduled_entries.append(scheduled_entry_context.context)
        rendered_scheduled_forms = render_to_string(template, {
            'scheduled_entries': scheduled_entries,
            'visit_attr': self.visit_model_attrname,
            'visit_model_instance': self.visit_model_instance,
            'app_label': self.visit_model_instance._meta.app_label,
            'registered_subject': self.registered_subject.pk,
            'appointment': self.appointment.pk,
            'dashboard_type': self.dashboard_type,
            'dashboard_model': self.dashboard_model_name,
            'dashboard_id': self.dashboard_id,
            'subject_dashboard_url': self.dashboard_url_name,
            'show': self.show})
        return rendered_scheduled_forms

    def render_requisitions(self):
        """Renders the Scheduled Requisitions section of the dashboard using the context class RequisitionContext."""
        template = 'scheduled_requisitions.html'
        scheduled_requisitions = []
        not_required_requisitions = []
        additional_requisitions = []
        show_not_required_requisitions = GlobalConfiguration.objects.get_attr_value('show_not_required_requisitions')
        allow_additional_requisitions = GlobalConfiguration.objects.get_attr_value('allow_additional_requisitions')
        show_drop_down_requisitions = GlobalConfiguration.objects.get_attr_value('show_drop_down_requisitions')
        requisition_helper = RequisitionMetaDataHelper(self.appointment, self.visit_model, self.visit_model_attrname)
        for scheduled_requisition in requisition_helper.get_entries_for('clinic'):
            requisition_context = RequisitionContext(scheduled_requisition, self.appointment, self.visit_model, self.requisition_model)
            if not show_not_required_requisitions and not requisition_context.required and not requisition_context.additional:
                not_required_requisitions.append(requisition_context.context)
            elif allow_additional_requisitions and not requisition_context.required and requisition_context.additional:
                additional_requisitions.append(requisition_context.context)  # TODO: is there a difference between added and additional?
            else:
                scheduled_requisitions.append(requisition_context.context)
        render_requisitions = render_to_string(template, {
            'scheduled_requisitions': scheduled_requisitions,
#             'not_required_requisitions': not_required_requisitions,
            'additional_requisitions': additional_requisitions,
            'drop_down_list_requisitions': self.drop_down_list_requisitions(scheduled_requisitions),
            'show_drop_down_requisitions': show_drop_down_requisitions,
            'visit_attr': self.visit_model_attrname,
            'visit_model_instance': self.visit_model_instance,
            'registered_subject': self.registered_subject.pk,
            'appointment': self.appointment.pk,
            'dashboard_type': self.dashboard_type,
            'dashboard_model': self.dashboard_model_name,
            'dashboard_id': self.dashboard_id,
            'subject_dashboard_url': self.dashboard_url_name,
            'show': self.show})
        return render_requisitions

    def drop_down_list_requisitions(self, scheduled_requisitions):
        drop_down_list_requisitions = []
        for requisition in scheduled_requisitions:
            lab_entry = requisition['lab_entry']
            meta_data_status = requisition['status']
            meta_data_required = meta_data_status != 'NOT_REQUIRED'
            if lab_entry.not_required and not lab_entry.additional:
                continue
            if not meta_data_required:
                drop_down_list_requisitions.append(requisition)
        return drop_down_list_requisitions

    def render_subject_hiv_status(self):
        """Renders to string a to a url to the historymodel for the subject_hiv_status."""
        if self.subject_hiv_status:
            change_list_url = reverse('admin:lab_tracker_historymodel_changelist')
            return render_to_string(self.subject_hiv_template, {
                'subject_hiv_status': self.subject_hiv_status,
                'subject_identifier': self.subject_identifier,
                'subject_type': self.subject_type,
                'change_list_url': change_list_url})

        return ''
