OUTGOING_SMS_STATUS = (
    ('new', 'New message'),
    ('sent', 'Message has been sent'),
    ('confirmed', 'Delivery report has been received'),
)

SMS_TYPE = (
    ('result', 'Result Message'),
    ('status', 'Status Message'),
    ('query', 'Query Message'),
    ('unauth', 'Unauthorized Message'),
    ('received', 'Received Message')
)

SMS_DELIVERY_REPORT = (
    ('1', 'Delivery success'),
    ('2', 'Delivery failure'),
    ('4', 'Message buffered'),
    ('8', 'Smsc submit'),
    ('16', 'Smsc reject'),
)
