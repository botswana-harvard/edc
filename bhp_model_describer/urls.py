from django.conf.urls import url, patterns

urlpatterns = patterns('',
    url(r'^(?P<app_label>\w+)/(?P<model_name>\w+)/$',
        'data_describer',
        name="describer_url_name"
        ),

    url(r'^counter/',
        'model_instance_counter',
        name="model_instance_counter_    url_name"
        ),

    url(r'',
        'data_describer',
        name="describer_url_name"
        ),
    )
