# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models


class LabCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"实验类名")
    desc = models.CharField(max_length=300, verbose_name=u"类别简介")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"实验类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Lab(models.Model):
    labcategory = models.ForeignKey(LabCategory, verbose_name=u"实验类名", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"实验")
    desc = models.CharField(max_length=300, verbose_name=u"实验描述")
    instance_module = models.CharField(max_length=50, verbose_name=u"虚拟机模板", null=True, blank=True)
    detail = models.TextField(verbose_name=u"实验详情", null=True, blank=True)
    degree = models.CharField(choices=(("cj", u"初级"), ("zj", u"中级"), ("gj", "高级")), verbose_name=u"实验难度", max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    image = models.ImageField(upload_to="image/%Y/%M", verbose_name=u"封面", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"实验"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
