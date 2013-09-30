from django.conf.urls.defaults import patterns, url

urlpatterns = patterns('',
    url(r'^viewresult/(?P<result_identifier>[0-9\-]+)/$',
        'view_result',
        name="view_result_report"
        ),
   )
