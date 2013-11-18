from django.conf.urls import patterns, url
from .views import generate_report, report_list, report_parameters, operational_report

urlpatterns = patterns('',
    url(r'^generate_report/', generate_report),
    url(r'^report_parameters/', report_parameters),
    url(r'^list/', report_list),
    #url(r'^operational/(?P<community>[a-z0-9\-\_\.]+)/(?P<date_from>[0-9{4}\/0-9{2}\/0-9{2}])/(?P<date_to>[0-9{4}\/0-9{2}\/0-9{2}])/', operational_report,),
    url(r'^operational/', operational_report,),
    )
