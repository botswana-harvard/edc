from django.http import HttpResponse
from django.conf import settings
from ..models import IncomingSms, Device
from ..classes import send_kannel_message, ServerSmsController, ClientSmsController
from ..sms_error_codes import (SUBJECT_IDENTIFIER_NOT_FOUND, SUBJECT_IDENTIFIER_FOUND)


def search_or_create_identifier(self, **kwargs):
    subject_identifier = None

    return subject_identifier


def receive_sms(request):
    controller = None
    valid_phone = True
    sender = request.GET['phone']
    text = request.GET['text']
    unallowed_phone = Device.objects.filter(phone__iexact=sender)
    if unallowed_phone:
        valid_phone = False

    elif not sender.lstrip("+").isdigit():
        valid_phone = False

    if valid_phone:
        msg = IncomingSms(phone=sender, text=text)
        msg.save()

        if settings.IS_SERVER:
            controller = ServerSmsController(True)
            result = controller.process_message(msg)
            if result['error_code'] == SUBJECT_IDENTIFIER_FOUND:
                controller.prepare_reply()
            elif result['error_code'] == SUBJECT_IDENTIFIER_NOT_FOUND:
                pass
            else:
                pass
        else:
            controller = ClientSmsController(True)
        '''
        result is dictionary containing error code and reply sms
        sent back to the client
        '''
        result = controller.process_message(msg)

        send_kannel_message(result['reply_msg'])
    return HttpResponse(result['reply_msg'])
