# -*-coding:utf8-*-
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


def show_group(request):
    response_dict = dict()
    response_dict["groups"] = ["温度传感器", "光敏光强传感器", "火焰传感器",
                              "光电对管", "气体传感器", "人体红外传感器"]
    response_dict["code"] = 200
    response_dict["msg"] = "success"
    json_response = json.dumps(response_dict)
    return HttpResponse(json_response, content_type="application/json")


def show_group_list(request, group_name=None):
    print(group_name)
    group_name = group_name
    client_reader = ClientReader()
    json_dict = dict()
    # json_dict["status_on"] = []
    # json_dict["status_off"] = []
    # x = "030B76562CFF0206"
    if group_name == "温度传感器":
        json_dict["status_on"] = [
            {"device_id": "030B76562CFF0205", "battery": 100},
        ]

        json_dict["status_off"] = [
            {"device_id": "030B76562CFF0208"},
            {"device_id": "030B76562CFF0209"},
            {"device_id": "030B76562CFF0210"}
        ]
        json_dict["code"] = 200
        json_dict["msg"] = "success"
        # for i in range
        # sensor_id_list = ["1234", "5678", "abcd", "efgh", "qwer"]
        all_device_status = client_reader.get_all_device_status()
        # for sensor_id in sensor_id_list:
        #     if sensor_id in all_device_status.keys():
        #         temp_dict = dict(sensor_id=sensor_id)
        #         temp_dict["battery"] = client_reader.get_battery_info(sensor_id)
        #         json_dict["status_on"].append(temp_dict)
        #     else:
        #         temp_dict = dict(sensor_id=sensor_id)
        #         json_dict["status_off"].append(temp_dict)
    elif group_name == "火焰传感器":
        json_dict["status_on"] = [
            {"device_id": "030B76562CFF0206", "battery": 50},
        ]

        json_dict["status_off"] = [
            {"device_id": "030B76562CFF0207"},
            {"device_id": "030B76562CFF0201"},
            {"device_id": "030B76562CFF0212"}
        ]
        json_dict["code"] = 200
        json_dict["msg"] = "success"
    elif group_name == "人体红外传感器":
        json_dict["status_on"] = [
            {"device_id": "030B76562CFF0106", "battery": 50},
        ]

        json_dict["status_off"] = [
            {"device_id": "030B76562CFF0107"},
            {"device_id": "030B76562CFF0101"},
            {"device_id": "030B76562CFF0112"}
        ]
        json_dict["code"] = 200
        json_dict["msg"] = "success"
    elif group_name == "光敏光强传感器":
        json_dict["status_on"] = [
            {"device_id": "030B76562CFF0306", "battery": 50},
        ]

        json_dict["status_off"] = [
            {"device_id": "030B76562CFF0307"},
            {"device_id": "030B76562CFF0301"},
            {"device_id": "030B76562CFF0312"}
        ]
        json_dict["code"] = 200
        json_dict["msg"] = "success"
    elif group_name == "光电对管":
        json_dict["status_on"] = [
            {"device_id": "030B76562CFF0406", "battery": 50},
        ]

        json_dict["status_off"] = [
            {"device_id": "030B76562CFF0407"},
            {"device_id": "030B76562CFF0401"},
            {"device_id": "030B76562CFF0412"}
        ]
        json_dict["code"] = 200
        json_dict["msg"] = "success"
    elif group_name == "气体传感器":
        json_dict["status_on"] = [
            {"device_id": "030B76562CFF0506", "battery": 50},
        ]

        json_dict["status_off"] = [
            {"device_id": "030B76562CFF0507"},
            {"device_id": "030B76562CFF0501"},
            {"device_id": "030B76562CFF0512"}
        ]
        json_dict["code"] = 200
        json_dict["msg"] = "success"
    else:
        return HttpResponse(json.dumps({"code": 404, "msg": "the group does not exist"},
                                       ensure_ascii=False, sort_keys=True, indent=4),
                            content_type="application/json")
    json_dict = json.dumps(json_dict, ensure_ascii=False, sort_keys=True, indent=4)
    return HttpResponse(json_dict, content_type="application/json")


def show_groups_list(request, group_name=None):
    group_name = group_name
    client_reader = ClientReader()
    sensor_id_dict = {"device_id": "da8f5209004b1200"}


def get_sensor_detail(request, sensor_id=None):
    sensor_id = sensor_id
    client_reader = ClientReader()
    for sensor_interface in ["40", "41", "42"]:
        sensor_key = sensor_id + ":" + sensor_interface
        try:
            json_dict = client_reader.get_sensor_info_value(sensor_key)
        except:
            return JsonResponse({"code": 404, "msg": "the sensor does not exist"})
        code_dict = {"code": 200, "msg": "success"}
        json_dict.update(code_dict)
        json_dict = json.dumps(json_dict, ensure_ascii=False, sort_keys=True, indent=4)
        return HttpResponse(json_dict, content_type="application/json")


def show_server_status(request):
    pass

