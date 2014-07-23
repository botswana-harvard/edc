from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from core.bhp_common.utils import os_variables
from .utils import all_uphosts


@login_required
def uphosts(request, **kwargs):
    template = 'uphosts.html'
    return render_to_response(template, {
        'report_title': 'HBC netbooks in the area',
        'section_name': kwargs.get('section_name'),
        'os_variables': os_variables,
        'uphosts': all_uphosts(**kwargs),
        'app_name': kwargs.get('app_name'),
    }, context_instance=RequestContext(request))
