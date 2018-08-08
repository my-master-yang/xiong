from datetime import datetime

from django.db import models


class InstanceList(models.Model):
    name = models.CharField(max_length=100, verbose_name=u"实例名")
    username = models.CharField(max_length=50, verbose_name=u"用户名")
    instanceID = models.CharField(max_length=100, verbose_name=u"实例ID")
    instanceST = models.CharField(max_length=50, verbose_name=u"实例状态")
    labID = models.IntegerField(default=0, verbose_name=u"实验ID")
    labName = models.CharField(max_length=50, verbose_name=u"实验名")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"活跃实例"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
