import os
import platform

from datetime import datetime

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings

from edc.apps.utils import Conf
from ..classes import SerializeToTransaction
from ..models import OutgoingTransaction

@login_required
def dump_to_usb(request, **kwargs):
    app_name = kwargs.get('app_name', None)
    site_name = Conf.return_site_name()
    if not site_name.islower():
        raise TypeError('Ensure settings.CURRENT_COMMUNITY is all small letters.')
    usb_path = None
    if platform.system() == 'Darwin':
        usb_path = '/Volumes/' + app_name + '_usb/'
    else:
        usb_path = '/media/' + app_name + '_usb/'
    if not app_name:
        raise ValidationError('app_name cannot be None')
    try:
        #filename should be in form appname_identifier_timestamp.jso eg bcpp_ranaka_2013118.json
        f = open(usb_path + app_name +'_'+ site_name + '_' + str(datetime.now().strftime("%Y%m%d%H%M")) + '.json', 'w')
    except:
        raise ValidationError('Please insert a usb device named \'{0}_usb\', currently using USB_PATH \'{1}\''.format(app_name, usb_path))
    outgoing_transactions = OutgoingTransaction.objects.filter(is_consumed_server=False, is_consumed_middleman=False)
    serializer = SerializeToTransaction()
    success = serializer.serialize_to_file(outgoing_transactions, f, True)
    f.close()
    for outgoing_transaction in outgoing_transactions:
        outgoing_transaction.is_consumed_middleman = True
        outgoing_transaction.consumer = usb_path
        outgoing_transaction.consumed_datetime = datetime.now()
        outgoing_transaction.save()
    if not success:
        messages.add_message(request, messages.ERROR, 'Serialization to path \'{0}\' failed'.format(usb_path))
    else:
        messages.add_message(request, messages.INFO, 'Serialized \'{0}\' \'{1}\' transactions to \'{2}\''.format(outgoing_transactions.count(), 'OutgoingTransactions', usb_path))
    return render_to_response(
        'dump_to_usb.html',
         context_instance=RequestContext(request)
        )
