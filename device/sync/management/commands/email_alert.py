from datetime import datetime, date
import socket
from optparse import make_option

from django.db.models import Count
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError

from ...models import IncomingTransaction


class Command(BaseCommand):
    """ Sends an email or sms notification to a list of recipients if not labs results have been
    imported into the local EDC 24 hrs
    """
    args = ('--email <email> --body <email_body>')

    help = 'Email any sync alerts'

    option_list = BaseCommand.option_list + (
        make_option(
            '--email',
            dest='email',
            action='store_true',
            default=False,
            help=('Send an email nofication.')),
     )

    def handle(self, *args, **options):
        #body = "No Statistics Provided"
        email_sender = 'django@bhp.org.bw'
        recipient_list = []
        stats = self.prepare_stats()

        tot = IncomingTransaction.objects.filter(is_consumed=False, is_ignored=False).count()
        body = "\nA summary of unconsumed incoming transactions"
        body += "\n{0} Incoming transactions\n".format(tot)
        if stats:
            body += "\nTotal:\t:Transaction name"
            body += "\n__________________________"
            for stat in stats:
                body += "\n{0}\t:{1}".format(stat['tx_count'], stat['tx_name'])
            body += "\n\t -------------------\t"

        if not args:
            CommandError('Invalid options, Try --help for a list of valid options')
        if options['email']:
            print args
            recipient_list = args[0].split(',')
            print "sending email to {0}".format(recipient_list)
            self.send_email(email_sender, recipient_list, body)
        else:
            raise CommandError('Unknown option, Try --help for a list of valid options')
        print "Successfully sent email to {0}".format(recipient_list)

    def send_email(self, email_sender, recipient_list, body):
        subject = "{0}, {1}: BCPP incoming transactions stats".format(socket.gethostname(), date.today())
        send_mail(subject, body, email_sender, recipient_list, fail_silently=False)

    def prepare_stats(self):
        return IncomingTransaction.objects.values('tx_name').filter(
            is_consumed=False, is_ignored=False
            ).annotate(
                tx_count=Count('tx_name')
                ).order_by('tx_name')