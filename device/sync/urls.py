from django.conf.urls import patterns, url, include
from .api import OutgoingTransactionMiddleManResource, OutgoingTransactionServerResource, MiddleManTransactionResource
from .views import index, view_transaction, consume_transactions

outgoing_transaction_middle_man_resource = OutgoingTransactionMiddleManResource()
outgoing_transaction_server_resource = OutgoingTransactionServerResource()
middle_man_transaction_resource = MiddleManTransactionResource()

urlpatterns = patterns('',
    (r'^api_otmr/', include(outgoing_transaction_middle_man_resource.urls)),
    (r'^api_otsr/', include(outgoing_transaction_server_resource.urls)),
    (r'^api_mmtr/', include(middle_man_transaction_resource.urls)),
    )

urlpatterns += patterns('',
    # The order is important, referred to from sync.urls and {app_name}_dispatch.urls
    url(r'^consume/(?P<producer>[a-z0-9\-\_\.]+)/(?P<app_name>[a-zA-Z\-\_\.]+)/', consume_transactions,),
    url(r'^consume/(?P<producer>[a-z0-9\-\_\.]+)/', consume_transactions,),
    url(r'^view/(?P<model_name>incomingtransaction|outgoingtransaction|middlemantransaction)/(?P<pk>[\w]{8}-[\w]{4}-[\w]{4}-[\w]{4}-[\w]{12})/', view_transaction, name='view_transaction_url',),
    url(r'^consumed/(?P<selected_producer>[a-z0-9\-\_\.]+)/', index,),
    url(r'^$', index,),
    )
