# !/usr/bin/python
# -*-coding:utf-8-*-
import random
import time
from all_utils import device_on

# class BatteryHandler:
#     battery_info = {}

#     def add_info(self, frame_body=None):
#         self.frame_body = frame_body

#     # 将电池信息存入字典
#     def handle_body(self):
#         frame_id, frame_value = self.parse_frame_body()
#         self.battery_info[frame_id] = frame_value

#     # 解析数据帧
#     def parse_frame_body(self):
#         frame_id = self.frame_body[0:16]
#         frame_value = int(self.frame_body[-2:], base=16)
#         return frame_id,  frame_value

#     # 返回电池信息
#     def get_value(self, frame_id):
#         if self.battery_info[frame_id]:
#             return self.battery_info[frame_id]
#         else:
#             return 100

# battery_handler = BatteryHandler()

if __name__ == "__main__":

    while True:
        value_index = random.randrange(0, 4, 1)
        value_hex = ["0", "25", "50", "75", "100"]
        sensor_id = "idcacb0a004b1200"
        # frame_body = sensor_id + str(value_hex[value_index])
        # print(frame_body)

        device_on[sensor_id] = value_hex[value_index]
        # battery_handler.parse_frame_body()
        # battery_handler.handle_body()

        # print(battery_handler.battery_info)
        print(device_on)
        time.sleep(10)
