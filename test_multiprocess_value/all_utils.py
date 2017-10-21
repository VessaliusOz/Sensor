# !usr/bin/python
# -*-coding:utf-8-*-
from write_data import battery_handler



class ClientReader:
    def get_battery_info(self, sensor_id):
        # 应该在redis里面保证每个设备id只保存一条信息   或者说，电池的信息不必用redis来存储
        # 这里的BatteryHandler是全局对象
        battery_handler = battery_handler
        battery = battery_handler.get_value(sensor_id)
        return battery if battery else "100"

