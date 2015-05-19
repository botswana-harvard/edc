from ..classes import send_kannel_message


class Sms(object):
    DELIMITER = " "

    def __init__(self, debug):
        self.result = {}
        if debug is None:
            self.debug = False
        else:
            self.debug = debug

    def send_reply(self, outgoing_sms):
        send_kannel_message(
            outgoing_sms.phone,
            outgoing_sms.text,
            outgoing_sms.id
            )

    def __explode_message(self):
        raise NotImplementedError("Should have implemented explode_message(...)")

    """Prepare text message to be sent to client.
    Prefix - A keyword to assist kannel route the sms to appropriate service (view)
    """
    def prepare_reply(self, prefix):
        raise NotImplementedError("Should have implemented prepare_reply(...)")

    """The child class should implement this method to validate the format of
    the sms received by its view e.g a netbook expects the sms to contain a
    token and subject idenfier separated by a delimiter
    """
    def __validate_get_identifier_sms(self, text):
        raise NotImplementedError("Should have implemented validate_get_identifier_sms(...)")

    """The child class should implement method to define what needs to be done
    where an sms is received by the view
    """
    def process_message(self, **kwargs):
        raise NotImplementedError("Should have implemented process_message(...)")
 
    def queue_message(self, phrase, message):
        """Queues a message targeted for a service identified by phrase."""
        from uuid import uuid4
        sms_queue_id = uuid4()
        return sms_queue_id
