from timer import device_on
import time


index = 0

while True:
    global index
    device_on[index] = index + 1
    index += 1
    print(device_on)
    time.sleep(1)
