import redis
import time
import json
import random


HOST = "localhost"
PORT = "6379"
r = redis.Redis(port=PORT, host=HOST)

while True:
    json_dict = {}
    json_dict["unix_timestamp"] = str(time.time())[0:10]
    json_dict["value"] = random.randint(10, 90)
    json_dict = json.dumps(json_dict, ensure_ascii=False)

    json2_dict = {}
    json2_dict["unix_timestamp"] = str(time.time())[0:10]
    json2_dict["value"] = random.randint(0, 1)
    json2_dict = json.dumps(json2_dict, ensure_ascii=False)

    json3_dict = {}
    json3_dict["unix_timestamp"] = str(time.time())[0:10]
    json3_dict["value"] = random.randint(10, 90)
    json3_dict = json.dumps(json3_dict, ensure_ascii=False)

    json4_dict = {}
    json4_dict["unix_timestamp"] = str(time.time())[0:10]
    json4_dict["value"] = random.randint(10, 90)
    json4_dict = json.dumps(json4_dict, ensure_ascii=False)

    json5_dict = {}
    json5_dict["unix_timestamp"] = str(time.time())[0:10]
    json5_dict["value"] = random.randint(10, 90)
    json5_dict = json.dumps(json5_dict, ensure_ascii=False)

    json6_dict = {}
    json6_dict["unix_timestamp"] = str(time.time())[0:10]
    json6_dict["value"] = random.randint(0, 1)
    json6_dict = json.dumps(json6_dict, ensure_ascii=False)

    r.lpush("030B76562CFF0205", json_dict)
    r.lpush("030B76562CFF0306", json3_dict)
    r.lpush("030B76562CFF0406", json4_dict)
    r.lpush("030B76562CFF0506", json5_dict)
    r.lpush("030B76562CFF0206", json2_dict)
    r.lpush("030B76562CFF0106", json6_dict)
    print(type(json_dict))
    time.sleep(2)
