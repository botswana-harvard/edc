from django.conf.urls import url, patterns

from .views import model_describer_view, model_instance_counter

urlpatterns = patterns('',
    url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/$',
        model_describer_view,
        name="model_describer_url_name"
        ),

    url(r'^(?P<app_label>\w+)/$',
        model_describer_view,
        name="model_describer_url_name"
        ),

    url(r'^counter/',
        model_instance_counter,
        name="model_instance_counter_url_name"
        ),

    url(r'',
        model_describer_view,
        name="model_describer_url_name"
        ),
    )
