from django.conf.urls import patterns, url

urlpatterns = patterns('',
    url(r'^generate_report/', 'generate_report'),
    url(r'^report_parameters/', 'report_parameters'),
    #url(r'^return_selectively/(?P<producer>[a-z0-9\-\_\.]+)/', 'return_selectively'),
    #url(r'^', 'return_items',),
    )
