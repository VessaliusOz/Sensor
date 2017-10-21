# -*-coding:utf8-*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.views.generic import TemplateView, FormView, DetailView
from django.contrib.auth import authenticate, login, logout
from sensor.forms import *
import json
from sensor.handle_database import ClientReader


class LoginView(TemplateView):
    def post(self, request):
        login_form = LoginForm(request.POST)
        if login_form.is_valid():
            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                login_info = {"if_login": 1}
                return JsonResponse(login_info)
            else:
                login_info = {"if_login": 0}
                return JsonResponse(login_info)
        else:
            login_info = {"if_login": 0}
            return JsonResponse(login_info)


def index(request):
    response_dict = dict()
    response_dict["type"] = ["group1", "group2", "group3"]
    json_response = json.dumps(response_dict)
    return HttpResponse(json_response, content_type="application/json")


def test_sensor_list(request, sensor_type=None):
    sensor_type = sensor_type
    client_reader = ClientReader()
    json_dict = dict()
    json_dict["status_on"] = []
    json_dict["status_off"] = []
    sensor_id_list = ["1234", "5678", "abcd", "efgh", "qwer"]
    all_device_status = client_reader.get_all_device_status()
    for sensor_id in sensor_id_list:
        if sensor_id in all_device_status.keys():
            temp_dict = dict(device_id=sensor_id)
            temp_dict["battery"] = client_reader.get_battery_info(sensor_id)
            json_dict["status_on"].append(temp_dict)
        else:
            temp_dict = dict(device_id=sensor_id)
            json_dict["status_off"].append(temp_dict)
    json_dict = json.dumps(json_dict, ensure_ascii=False, sort_keys=True, indent=4)
    return HttpResponse(json_dict, content_type="application/json")


def test_sensor_detail(request, sensor_type=None, sensor_id=None):
    sensor_type = sensor_type
    sensor_id = sensor_id
    client_reader = ClientReader()
    json_dict = json.dumps(client_reader.get_sensor_info_value(sensor_id), ensure_ascii=False, sort_keys=True, indent=4)
    return HttpResponse(json_dict, content_type="application/json")


def yaoji_index(request):
    response_dict = dict()
    response_dict["group"] = ["group1", "group2", "group3"]
    json_response = json.dumps(response_dict)
    return HttpResponse(json_response, content_type="application/json")


def yaoji_sensor_list(request, sensor_type=None):
    json_dict = dict()
    json_dict["status_on"] = [
        {"device_id": "030B76562CFF0201", "battery": 100},
        {"device_id": "030B76562CFF0202", "battery": 75},
        {"device_id": "030B76562CFF0203", "battery": 25}
    ]

    json_dict["status_off"] = [
        {"device_id": "030B76562CFF0205"},
        {"device_id": "030B76562CFF0206"},
        {"device_id": "030B76562CFF0207"}
    ]
    json_dict = json.dumps(json_dict, ensure_ascii=False, sort_keys=True, indent=4)
    return HttpResponse(json_dict, content_type="application/json")


def yaoji_sensor_detail(request, sensor_type=None, sensor_id=None):
    json_dict = {
        "datetime": "2017-10-07 16:52:44",
        "value": 36
    }
    json_dict = json.dumps(json_dict, ensure_ascii=False, sort_keys=True, indent=4)
    return HttpResponse(json_dict, content_type="application/json")
