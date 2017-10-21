from django.conf.urls import url
from django.contrib import admin
# from sensor.views import *
from sensor.test_view import *
from sensor.views import *


urlpatterns = [
    url(r'^login', LoginView.as_view()),
    url(r'^group/$', show_group),
    # url(r"^index/(?P<sensor_type>.+)", get_sensor_list),
    url(r"^device/(?P<sensor_id>.+)/$", get_sensor_detail),
    url(r"^group/(?P<group_name>.+)/$", show_group_list),

    # url(r"^index/(?P<sensor_type>.+)/(?P<sensor_id>.+)", get_sensor_detail),
]
