# encoding:utf8
import redis
import json
from datetime import datetime
import pymysql
import time
import struct


class BatteryRedis:
    redis_pool = None
    HOST = "localhost"
    PORT = 6379

    def __init__(self, frame_body=None):
        self.frame_body = frame_body
        self.__redis_conn = None

    def insert_into_redis(self):
        frame_id, frame_value = self.parse_frame_body()
        self.redis_pool = self.redis_pool or redis.ConnectionPool(host=self.HOST, port=self.PORT)
        self.__redis_conn = redis.Redis(connection_pool=self.redis_pool)
        # 就让redis里面只存一条数据,存的就是电池的dict
        # 数据处理

        battery_info = self.__redis_conn.rpop("battery_info") or "{}"
        battery_info_dict = json.loads(battery_info)
        battery_info_dict[frame_id] = frame_value
        self.__redis_conn.lpush("battery_info", json.dumps(battery_info_dict))

    def parse_frame_body(self):
        frame_id = self.frame_body[0:16]
        frame_value = int(self.frame_body[-2:], base=16)
        return frame_id,  frame_value


class HeartBeatRedis:
    redis_pool = None
    HOST = "localhost"
    PORT = 6379

    def __init__(self, frame_body=None):
        self.frame_body = frame_body
        self.__redis_conn = None

    def insert_into_redis(self):
        frame_id, coordinator_id, net_standard = self.parse_frame_body()
        self.redis_pool = self.redis_pool or redis.ConnectionPool(host=self.HOST, port=self.PORT)
        self.__redis_conn = redis.Redis(connection_pool=self.redis_pool)
        # 就让redis里面只存一条数据,存的就是电池的dict
        # 数据处理
        heartbeat_info = self.__redis_conn.rpop("heartbeat_info") or json.dumps({})
        heartbeat_info_dict = json.loads(heartbeat_info)
        heartbeat_info_dict[frame_id] = {"net_standard": net_standard, "coordinator_id": coordinator_id}
        self.__redis_conn.lpush("heartbeat_info", json.dumps(heartbeat_info_dict))

    def parse_frame_body(self):
        frame_id = self.frame_body[0:16]
        coordinator_id = self.frame_body[-16:]
        net_standard = self.frame_body[17, 19]
        return frame_id, coordinator_id, net_standard


class HeartBeatUpdater:
    redis_pool = None
    HOST = "localhost"
    PORT = 6379

    def update(self):
        self.redis_pool = self.redis_pool or redis.ConnectionPool(host=self.HOST, port=self.PORT)
        redis_conn = redis.Redis(connection_pool=self.redis_pool)
        redis_conn.rpop("heartbeat_info")
        redis_conn.lpush("heartbeat_info", "{}")


class SensorInfoRedis:

    redis_pool = None
    HOST = "localhost"
    PORT = 6379

    def __init__(self, frame_body=None, sensor_interface=None):
        self.frame_body = frame_body
        self.sensor_interface = sensor_interface
        self.__redis_conn = None

    def insert_into_redis(self):
        frame_id, frame_unix_timestamp, frame_value = self.parse_frame_body()
        self.redis_pool = self.redis_pool or redis.ConnectionPool(host=self.HOST, port=self.PORT)
        self.__redis_conn = redis.Redis(connection_pool=self.redis_pool)
        info = dict()
        info["time"] = frame_unix_timestamp
        info["value"] = frame_value
        # 改变了redis的key,将sensor_id 和 interface联系在了一起，至于怎样的处理应该交给view函数来处理
        redis_key = self.frame_body + ":" + self.sensor_interface
        # 到底是lpush还是rpush，　应该都无所谓的
        self.__redis_conn.lpush(redis_key, json.dumps(info))

    def parse_frame_body(self):
        frame_id = self.frame_body[0:16]
        frame_unix_timestamp = int(self.frame_body[-8:], base=16)
        frame_value = int(self.frame_body[16:-8], base=16)
        return frame_id, frame_unix_timestamp, frame_value


class ClientReader:
    redis_pool = None
    HOST = "localhost"
    PORT = 6379
    device_on = {}

    def __init__(self, duration=600):
        self.__redis_conn = None
        self.duration = duration

    def get_sensor_info_value(self, sensor_key):
        self.redis_pool = self.redis_pool or redis.ConnectionPool(host=self.HOST, port=self.PORT)
        self.__redis_conn = redis.Redis(connection_pool=self.redis_pool)
        data = self.__redis_conn.lindex(sensor_key, 0).decode("ascii")
        temp_value_dict = json.loads(data)
        # 前端来处理
        return temp_value_dict

    def get_battery_info(self, sensor_id):
        self.redis_pool = self.redis_pool or redis.ConnectionPool(host=self.HOST, port=self.PORT)
        self.__redis_conn = redis.Redis(connection_pool=self.redis_pool)
        battery_info = self.__redis_conn.lindex("batter_info", 0).decode("ascii")
        battery_info_dict = json.loads(battery_info)
        battery_value = battery_info_dict[sensor_id] or 100
        return battery_value

    def get_device_status(self, sensor_id):
        self.redis_pool = self.redis_pool or redis.ConnectionPool(host=self.HOST, port=self.PORT)
        self.__redis_conn = redis.Redis(connection_pool=self.redis_pool)
        status_info = self.__redis_conn.lindex("heartbeat_info", 0).decode("ascii")
        status_info_dict = json.loads(status_info)
        if sensor_id in status_info_dict.keys():
            return True
        else:
            return False

    def get_all_device_status(self):
        pass


# 抽象工厂
# 要写三个关于sensor_type的类，我觉得没毛病
def connect_to_redis(data_type, body):
    frame_type = data_type
    frame_body = body
    if frame_type == "20":
        frame_handler = BatteryRedis(frame_body=frame_body)
    # 如果它准备显示三条曲线，那就应该区分是哪个传感器接口传递的数据，没有更好的办法么
    elif frame_type == "40" or frame_type == "41" or frame_type == "42":
        frame_handler = SensorInfoRedis(frame_body=frame_body, sensor_interface=frame_type)
    elif frame_type == "00":
        frame_handler = HeartBeatRedis(frame_body=frame_type)
    else:
        raise ValueError("wrong package type")
    return frame_handler


class MysqlHandler:

    def __init__(self):
        pass

    def search(self, from_time, end_time):
        if from_time and end_time:
            pass
        else:
            return "args is not completed"





