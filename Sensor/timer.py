import threading
import time
from abc import ABCMeta, abstractmethod


class BaseTimer(threading.Thread):

    __metaclass__ = ABCMeta

    def __init__(self, howtime=1.0, enduring=True):
        self.howtime = howtime
        self.enduring = enduring
        threading.Thread.__init__(self)

    def run(self):
        time.sleep(self.howtime)
        self.exec()
        while self.enduring:
            time.sleep(self.howtime)
            self.exec()

    @abstractmethod
    def exec(self):
        pass

    def destory(self):
        self.enduring = False
        del self

    def restart(self):
        self.enduring = True

    def stop(self):
        self.enduring = False

    def get_status(self):
        return self.enduring


class TimerMask(BaseTimer):

    def __init__(self, howtime=1.0, enduring=True):
        BaseTimer.__init__(self, howtime, enduring)

    def exec(self):
        print("about to clean")
        device_on.clear()
        print(device_on)
        print("successful")


device_on = {}

Timer = TimerMask(howtime=10)
print("begin")
Timer.start()


