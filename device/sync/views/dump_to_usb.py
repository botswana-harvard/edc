import os
import platform
from datetime import datetime
from django.core.exceptions import ValidationError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from ..models import OutgoingTransaction
from ..classes import SerializeToTransaction


@login_required
def dump_to_usb(request, **kwargs):
    app_name = kwargs.get('app_name',None)
    usb_path = None
    if platform.system() == 'Darwin':
        usb_path = '/Volumes/'+app_name+'_usb/'
    else:
        usb_path = ''
    if not app_name:
        raise ValidationError('app_name cannot be None')
    try:
        f = open(usb_path+app_name+'_'+str(datetime.now().strftime("%Y-%m-%d%H%M"))+'.json','w')
    except:
        raise ValidationError('Please insert a usb device named \'{0}_usb\', currently using USB_PATH \'{1}\''.format(app_name,usb_path))
    outgoing = OutgoingTransaction.objects.filter(is_consumed_server=False)
    serializer = SerializeToTransaction()
    success = serializer.serialize_to_file(outgoing, f, True)
    f.close()
    for ot in outgoing:
        ot.is_consumed_middleman = True
        ot.save()
    if not success:
        messages.add_message(request, messages.ERROR, 'Serialization to path \'{0}\' failed'.format(usb_path))
    else:
        messages.add_message(request, messages.INFO, 'Serialized \'{0}\' \'{1}\' transactions to \'{2}\''.format(outgoing.count(),'OutgoingTransactions',usb_path))  
    return render_to_response(
        'dump_to_usb.html',
         context_instance=RequestContext(request)
        )
