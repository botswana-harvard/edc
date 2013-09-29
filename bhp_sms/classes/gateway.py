import urllib2
import urllib
from django.conf import settings


def send_kannel_message(number, text, msgid):
    dlr_url = urllib.quote_plus('http://localhost:8080/messaging/dlr/?msgid=' + str(msgid)+'&report=%d')
    msg_url = 'http://localhost:' + settings.KANNEL_PORT + '/cgi-bin/sendsms?username=' + settings.KANNEL_USERNAME+'&password='+settings.KANNEL_PASSWORD+'&to='+number+'&text='+urllib.quote_plus(text)+'&dlr-url='+dlr_url+'&dlr-mask=31'
#    page = msg_url
    page = urllib2.urlopen(msg_url).read()
    return page
