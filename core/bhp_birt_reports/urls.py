from django.conf.urls import patterns, url
from .views import generate_report, report_list, report_parameters, operational_report

urlpatterns = patterns('',
    url(r'^generate_report/', generate_report),
    url(r'^report_parameters/', report_parameters),
    url(r'^list/', report_list),
    url(r'^operational', operational_report,),
    )
