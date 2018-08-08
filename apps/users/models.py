# _*_ encoding:utf-8 _*_

from django.contrib.auth.models import AbstractUser
from django.db import models

from courses.models import Course
from examination.models import ExamLesson
from experiment.models import Lab
from datetime import datetime, timedelta

class UserProfile(AbstractUser):
    """
    只是为了后台登录而用
    """

    class Meta:
        verbose_name = u"用户信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username


class Personal_info(models.Model):
    """
    个人信息
    """
    username = models.CharField(max_length=50, verbose_name=u"用户名", default="")
    nick_name = models.CharField(max_length=50, verbose_name=u"姓名", null=True, blank=True)
    birthday = models.CharField(max_length=50, verbose_name=u"生日", null=True, blank=True)
    gender = models.CharField(max_length=6, choices=(('male', u"男"), ('female', u"女")), null=True, blank=True)
    mobile = models.CharField(max_length=20, null=True, blank=True)
    qq_number = models.CharField(max_length=20, null=True, blank=True)
    email = models.CharField(max_length=20, null=True, blank=True)

    class Meta:
        verbose_name = u"个人信息"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.nick_name


class UserExamination(models.Model):
    """
    记录历史考试模板
    """
    username = models.CharField(max_length=50, verbose_name=u"用户名", default="")
    examlesson = models.ForeignKey(ExamLesson, verbose_name=u"试卷")
    score = models.IntegerField(verbose_name=u"总分", default=0)
    exam_times = models.IntegerField(default=0, verbose_name=u"考试时长时长（分钟数）")

    frist_time = models.DateTimeField(default=datetime(2017, 1, 1, 1, 1, 1, 1), verbose_name="第一次添加时间")

    class Meta:
        verbose_name = u"历史试卷"
        verbose_name_plural = verbose_name


class LabCollection(models.Model):
    """
    实验收藏模板
    """
    username = models.CharField(max_length=50, verbose_name=u"用户名", default="")
    labpk = models.IntegerField(default=0, verbose_name=u"实验课程id")
    name = models.CharField(max_length=50, verbose_name=u"实验课程", default="")
    level = models.CharField(max_length=50, verbose_name=u"难度", default="")

    # image = models.CharField(max_length=50,verbose_name=u"封面",default="")

    class Meta:
        verbose_name = u"收藏实验"
        verbose_name_plural = verbose_name


class LessonCollection(models.Model):
    """
    课程收藏模板
    """
    username = models.CharField(max_length=50, verbose_name=u"用户名", default="")
    coursepk = models.IntegerField(default=0, verbose_name=u"学习课程id")
    name = models.CharField(max_length=50, verbose_name=u"学习课程", default="")
    level = models.CharField(max_length=50, verbose_name=u"难度", default="")

    class Meta:
        verbose_name = u"收藏课程"
        verbose_name_plural = verbose_name


# #学习课程模板
# class Lesson_studied(models.Model):
#     username = models.CharField(max_length=50, verbose_name=u"用户名", default="")
#     coursepk = models.IntegerField(default=0, verbose_name=u"学习课程id")
#
# #学习实验模板
# class Lab_studied(models.Model):
#     username = models.CharField(max_length=50, verbose_name=u"用户名", default="")
#     coursepk = models.IntegerField(default=0, verbose_name=u"学习实验id")
#
