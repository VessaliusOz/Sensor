import socket
import time
import redis
from datetime import datetime
import json


redis_conn = redis.Redis(host="localhost", port=6379)

value = 15

while True:
    temp_unix = str(time.time())[0:10]
    date_time = datetime.fromtimestamp(int(temp_unix))
    global value
    info = dict(datetime=str(date_time), value=value)
    print(info)
    redis_conn.lpush("abcd", json.dumps(info))
    value += 1
    time.sleep(2)

