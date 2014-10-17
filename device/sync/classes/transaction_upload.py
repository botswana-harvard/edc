from datetime import datetime
import socket


class TransactionUpload(object):

    def compile_upload_stats(self, args, upload_file_model):
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
            uploaded = upload_file_model.objects.get(file_name=entry)
            body += "\nSUCCESS:\t{0}, uploaded={1}, duplicates={2}, ".format(entry, uploaded.consumed, uploaded.not_consumed)
        for entry in error_list:
            body += "\nERROR:\t{0}".format(entry)
        print "sending email to {0}".format(recipient_list)
        return (subject, body, recipient_list)