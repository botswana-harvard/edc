from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response
from django.template import RequestContext

from ..models import BaseReport


@login_required
def report_list(request, **kwargs):
    reports = BaseReport.objects.all()

    return render_to_response(
        'report_list.html', {'reports': reports},
        context_instance=RequestContext(request)
        )
