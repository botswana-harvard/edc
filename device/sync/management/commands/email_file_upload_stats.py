from datetime import datetime
import socket
from optparse import make_option

from django.db.models import get_model
from django.core.mail import send_mail
from django.core.management.base import BaseCommand, CommandError


class Command(BaseCommand):
    """ Sends an email to a list of recipients about the status of uploading transaction files
    """
    args = ('--success <comma_separated> --error <comma_separated> --email <comma_separated>')

    help = 'Email transaction file upload stats'

    option_list = BaseCommand.option_list + (
        make_option(
            '--success',
            dest='success',
            action='store_true',
            default=False,
            help=('Comma separated list of successfully uploaded files names.')),
        make_option(
            '--error',
            action='store_true',
            dest='error',
            default=False,
            help=('Comma separated list of files that failed to upload')),
         make_option(
            '--email',
            action='store_true',
            dest='email',
            default=False,
            help=('Comma separated list of reciepant\'s emails')),
        )

    def handle(self, *args, **options):
        email_sender = 'django@bhp.org.bw'
        UploadTransactionFile = get_model('import', 'UploadTransactionFile')
        sucess_list = []
        error_list = []
        recipient_list = []
        if not len(args) == 3:
            raise CommandError('Please input arguments in this form--success <[]> --error <[]> --email <comma_separated>')
        if options['email'] and options['success'] and options['error']:
            sucess_list = args[0].split(',')
            error_list = args[1].split(',')
            print args
            if (len(error_list) == 1 and error_list[0].lower() == 'none') and (len(sucess_list) == 1 and sucess_list[0].lower() == 'none'):
                #python manage.py email_file_upload_stats --success None --error None--email opharatlhatlhe@bhp.org.bw
                subject = 'NOTHING: {0} {1} No upload file found'.format(datetime.today().strftime('%Y%m%d%H%M'), socket.gethostname())
                sucess_list.pop()
                error_list.pop()
            elif len(error_list) == 1 and error_list[0].lower() == 'none':
                #python manage.py email_file_upload_stats --success bcpp_lentswe_201410081525.json --error bcpp_letlha_201410081525.json --email opharatlhatlhe@bhp.org.bw
                #len(error_list) can never be zero.
                subject = 'SUCCESS: {0} {1} Upload transaction files stats'.format(datetime.today().strftime('%Y%m%d%H%M'), socket.gethostname())
                error_list.pop()
            else:
                #python manage.py email_file_upload_stats --success bcpp_lentswe_201410081525.json --error None --email opharatlhatlhe@bhp.org.bw
                subject = 'ERROR: {0} {1} Upload transaction files stats'.format(datetime.today().strftime('%Y%m%d%H%M'), socket.gethostname())
            recipient_list = args[2].split(',')
            body = "\nUploaded incoming transaction files:"
            body += "\n______________________________________"
            for entry in sucess_list:
                if entry.lower() == 'none':
                    #This is the case that not attempted upload was successful i.e
                    #python manage.py email_file_upload_stats --success None --error bcpp_letlha_201410081525.json --email opharatlhatlhe@bhp.org.bw
                    break
                uploaded = UploadTransactionFile.objects.get(file_name=entry)
                body += "\nSUCCESS:\t{0}, uploaded={1}, duplicates={2}, ".format(entry, uploaded.consumed, uploaded.not_consumed)
            for entry in error_list:
                body += "\nERROR:\t{0}".format(entry)
            print "sending email to {0}".format(recipient_list)
            # TODO: if connection is not up the report will not be delivered
            # e.g. no retry -- what about using edc.notification
            self.send_email(email_sender, subject, body, recipient_list)
        else:
            raise CommandError('Unknown option, Try --help for a list of valid options')
        print "Successfully sent email to {0}".format(recipient_list)

    def send_email(self, email_sender, subject, body, recipient_list):
        send_mail(subject, body, email_sender, recipient_list, fail_silently=False)
