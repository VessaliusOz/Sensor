# !/usr/bin/python
# -*-coding:utf-8-*-
# from all_utils import ClientReader
import time
from write_data import battery_handler

class ClientReader:
    def get_battery_info(self, sensor_id):
        # 应该在redis里面保证每个设备id只保存一条信息   或者说，电池的信息不必用redis来存储
        # 这里的BatteryHandler是全局对象
        from write_data import battery_handler
        
        battery_handler = battery_handler
        battery = battery_handler.get_value(sensor_id)
        return battery if battery else "100"




print("enter the get_process")



class Viewer:

    def __init__(self, sensor_id):
        print("initial---------")
        self.sensor_id = sensor_id

    def get_response_value(self):
        client = ClientReader() 
        print(client.get_battery_info(self.sensor_id))


viewer = Viewer("1dcacb0a004b1200")
while True:
    viewer.get_response_value()
    while True:
        print("gg")
        viewer.get_response_value()
        time.sleep(2)
