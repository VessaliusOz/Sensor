from django.db import models
from django.contrib.auth.models import User
from django.utils.datetime_safe import datetime


class SensorGroup(models.Model):
    group_name = models.CharField(max_length=20, default=None, null=True, blank=True, verbose_name="分组")
    user = models.ForeignKey(User, verbose_name="用户", default=None, null=True)
    parse_bit_number = models.IntegerField(default=0, null=True, blank=True, verbose_name="小数点位数")

    def __str__(self):
        return self.group_name


class Sensor(models.Model):
    sensor_name = models.CharField(max_length=20, default=None, null=True, blank=True, verbose_name="设备名称")
    sensor_id = models.CharField(max_length=16, default=None, null=True, blank=True, verbose_name="设备ID")
    sensor_type = models.CharField(max_length=10, default=None, null=True, blank=True, verbose_name="设备类型")
    datetime = models.DateTimeField(default=datetime.now, verbose_name="上传时间")
    group = models.ForeignKey(SensorGroup, default=None, null=True, blank=True, verbose_name="所在分组")

    def __str__(self):
        return self.sensor_name


class SensorData(models.Model):
    unix_time = models.IntegerField(default=0, null=True, blank=True, verbose_name="unix时间戳")
    value = models.IntegerField(default=0, null=True, blank=True, verbose_name="数值")
    sensor = models.ForeignKey(Sensor, default=None, null=True, verbose_name="传感器")
    related_interface = models.IntegerField(default=0, null=True, blank=True, verbose_name="传感器接口")

    def __str__(self):
        return self.related_interface


