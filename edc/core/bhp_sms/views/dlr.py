from django.http import HttpResponse
from django.core.exceptions import ObjectDoesNotExist
from ..models import SmsDlr, OutgoingSms


def receive_dlr(request):
    msgid = str(request.GET['msgid'])
    status = str(request.GET['report'])

    try:
        msg = OutgoingSms.objects.get(pk=msgid)
        msg.is_delivered = True
        dlr = SmsDlr(sms=msg, status=status)
        dlr.save()
        response = "dlr: {0} - {1}".format(msgid, status)
    except ObjectDoesNotExist:
        response = "sms not found"

    return HttpResponse(response)
