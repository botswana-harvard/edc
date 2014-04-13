import json

from datetime import datetime

from smtplib import SMTPException

from django.core.management.base import BaseCommand, CommandError
from django.core.mail import send_mail


from ...models import Notification


class Command(BaseCommand):

    args = '<message_tag>'
    help = 'Export transactions for a given app_label.model_name.'
    option_list = BaseCommand.option_list

    def handle(self, *args, **options):
        for notification in Notification.objects.filter(sent=False):
            try:
                print 'sending to {0}'.format(', '.join(json.loads(notification.recipient_list) + json.loads(notification.cc_list)))
                send_mail(notification.subject,
                          notification.body,
                          'edcdev@bhp.org.bw',
                          json.loads(notification.recipient_list) + json.loads(notification.cc_list),
                          fail_silently=False)
            except SMTPException as e:
                print 'Unable to send notification. {2}. See \'{0}\' pk={1}'.format(notification.subject, notification.pk, e)
            else:
                notification.sent = True
                notification.sent_datetime = datetime.today()
