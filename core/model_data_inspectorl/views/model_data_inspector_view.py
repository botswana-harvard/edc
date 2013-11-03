from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from edc.core.model_selector.classes import ModelSelector
from edc.core.model_selector.forms import ModelSelectorForm

from ..classes import ModelDataInspector


@login_required
def model_data_inspector_view(request, **kwargs):

    section_name = kwargs.get('section_name')
    report_title = 'Model Data Summary and Description'
    template = 'model_data_inspector.html'
    form = ModelSelectorForm()
    context = {
        'form': form,
        'table': '',
        'section_name': section_name,
        'report_title': report_title,
        'report': '',
        'report_name': kwargs.get('report_name'),
        }
    if request.method == 'POST':
        form = ModelSelectorForm(request.POST)
        if form.is_valid():
            app_label = form.cleaned_data.get('app_label')
            model_name = form.cleaned_data.get('model_name')
            model_selector = ModelSelector(app_label, model_name)
            model_data_inspector = ModelDataInspector(app_label, model_name)
            if model_data_inspector.get_model():
                summary = model_data_inspector.summarize()
                group = model_data_inspector.group()
                group_m2m = model_data_inspector.group_m2m()
                context = {
                    'form': form,
                    'app_label': model_selector.get_app_label(),
                    'model_name': model_selector.get_model_name(),
                    'app_labels': model_selector.get_app_labels(),
                    'model_names': model_selector.get_model_names(),
                    'summary_fields': summary['fields'],
                    'group_fields': group['fields'],
                    'group_m2m_fields': group_m2m['fields'],
                    'fields': model_data_inspector.get_model()._meta.fields,
                    'section_name': section_name,
                    'report_title': report_title,
                    'cumulative_frequency': 0,
                    }
    else:
        form = ModelSelectorForm()
        model_selector = None
    return render_to_response(template, context, context_instance=RequestContext(request))
