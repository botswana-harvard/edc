from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^return/(?P<producer>[a-z0-9\-\_\.]+)/', 'return_items'),
    url(r'^return/(?P<identifier>\w+)/', 'return_households', name='return_household'),
    url(r'^return/(?P<identifier>\w+)/', 'return_households', name='return_household'),
    )
