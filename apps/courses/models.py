# _*_ encoding:utf-8 _*_
from datetime import datetime

from django.db import models


# 课程类别
class CourseCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"课程类名")
    desc = models.CharField(max_length=300, verbose_name=u"类别简介")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Course(models.Model):
    coursecategory = models.ForeignKey(CourseCategory, verbose_name=u"课程类别", null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"课程")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程"
        verbose_name_plural = verbose_name

    def __str__(self):
        return u"{0}(课程名:{1})".format(self.coursecategory.name, self.name)


# class Chapter(models.Model):
#     coursecategory = models.ForeignKey(CourseCategory, verbose_name=u"课程类别", null=True, blank=True)
#     course = models.ForeignKey(Course, verbose_name=u"课程",null=True,blank=True)
#     name = models.CharField(max_length=50, verbose_name=u"章节")
#     add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
#
#     class Meta:
#         verbose_name = u"章节"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return u"{0}(课程名:{1}|章节名：{2})".format(self.coursecategory.name, self.course.name, self.name)


class Lesson(models.Model):
    coursecategory = models.ForeignKey(CourseCategory, verbose_name=u"课程类别", null=True, blank=True)
    course = models.ForeignKey(Course, verbose_name=u"课程", null=True, blank=True)
    # chapter = models.ForeignKey(Chapter, verbose_name=u"章节",null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u"小节")
    desc = models.CharField(max_length=300, verbose_name=u"小节描述")
    detail = models.TextField(verbose_name=u"小节详情", null=True, blank=True)
    degree = models.CharField(choices=(("cj", u"初级"), ("zj", u"中级"), ("gj", "高级")), verbose_name=u"小节难度", max_length=2)
    learn_times = models.IntegerField(default=0, verbose_name=u"学习时长（分钟数）")
    students = models.IntegerField(default=0, verbose_name=u"学习人数")
    image = models.ImageField(upload_to="image/%Y/%M", verbose_name=u"封面", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"小节"
        verbose_name_plural = verbose_name

    def __str__(self):
        # return u"{0}(课程名:{1}|章节名：{2}|小节{3})".format(self.coursecategory.name, self.course.name, self.chapter.name, self.name)
        return u"{0}(课程名:{1}|小节{2})".format(self.coursecategory.name, self.course.name, self.name)


# # 资源
# class CourseResource(models.Model):
#     course = models.ForeignKey(Course, verbose_name=u"课程")
#     name = models.CharField(max_length=100, verbose_name=u"名称")
#     download = models.FileField(upload_to="course/resourse/%Y/%M", verbose_name=u"资源文件", max_length=100)
#     add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
#
#     class Meta:
#         verbose_name = u"课程资源"
#         verbose_name_plural = verbose_name
#
#     def __str__(self):
#         return self.name
