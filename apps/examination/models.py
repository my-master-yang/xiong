# _*_ encoding:utf-8 _*_
from datetime import datetime, timedelta

from django.db import models


# 课程类别
class ExamCategory(models.Model):
    name = models.CharField(max_length=50, verbose_name=u"课程类名")
    desc = models.CharField(max_length=300, verbose_name=u"类别简介")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"课程类别"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


# 考试科目
class ExamLesson(models.Model):
    examcategory = models.ForeignKey(ExamCategory, verbose_name=u'课程类名', null=True, blank=True)
    name = models.CharField(max_length=50, verbose_name=u'考试科目')
    desc = models.CharField(max_length=300, verbose_name=u"科目描述")
    # detail = models.TextField(verbose_name=u"考试详情", null=True, blank=True)
    degree = models.CharField(choices=(("cj", u"初级"), ("zj", u"中级"), ("gj", "高级")), verbose_name=u"科目难度", max_length=2)
    students = models.IntegerField(default=0, verbose_name=u"考试人数")
    image = models.ImageField(upload_to="image/%Y/%M", verbose_name=u"考试封面", max_length=100)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")
    exam_times = models.IntegerField(default=0, verbose_name=u"考试时长时长（分钟数）")

    class Meta:
        verbose_name = u'考试科目'
        verbose_name_plural = verbose_name

    def __str__(self):
        return u"{0}(考试科目:{1})".format(self.examcategory.name, self.name)

class AnswerCard(models.Model):
    user_name = models.CharField(max_length=20, verbose_name="u姓名", null=True, blank=True)
    number_id = models.IntegerField(verbose_name=u"试卷编号", null=True, blank=True)
    start_time = models.DateTimeField(verbose_name=u"开始时间", default=datetime.now(), null=True, blank=True)



# 题库
class Question(models.Model):
    examcategory = models.ForeignKey(ExamCategory, verbose_name=u'课程类名', null=True, blank=True)
    examLessonNum = models.IntegerField(verbose_name='试卷编号', blank=False, default=1)
    # questionNum = models.IntegerField(verbose_name='题目编号',default=1)
    questionType = models.CharField(max_length=2, choices=(("xz", u"选择题"), ("pd", u"判断题")))
    content = models.TextField(verbose_name=u"题目内容")
    OptionA = models.TextField(verbose_name=u"A选项字段", blank=True)
    OptionB = models.TextField(verbose_name=u"B选项字段", blank=True)
    OptionC = models.TextField(verbose_name=u"C选项字段", blank=True)
    OptionD = models.TextField(verbose_name=u"D选项字段", blank=True)
    answer = models.CharField(max_length=50, verbose_name=u"正确答案")
    boolt = models.TextField(verbose_name=u"判断题正确", default=u"正确")
    boolf = models.TextField(verbose_name=u"判断题错误", default=u"错误")
    score = models.IntegerField(verbose_name=u"本题分值", default=0)
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"题库"
        verbose_name_plural = verbose_name

    def get_content_display(self, field):
        return self.content

    def __str__(self):
        model = Question
        return "{0}(题干:{1}|正确答案:{2})".format(self.examcategory.name, self.content, self.answer)


# 本套考试试卷的试题列表
class ExamPaper(models.Model):
    examcategory = models.ForeignKey(ExamCategory, verbose_name=u"课程类名")
    examlesson = models.ForeignKey(ExamLesson, verbose_name=u"考试科目")
    examLessonNum = models.IntegerField(verbose_name='试卷编号', blank=False, default=1)
    # question = models.ForeignKey(Question, verbose_name=u"题目")
    examFile = models.FileField(verbose_name='考试试卷文件', upload_to="file/", default="/file/")
    add_time = models.DateTimeField(default=datetime.now, verbose_name=u"添加时间")

    class Meta:
        verbose_name = u"试题列表"
        verbose_name_plural = verbose_name

    def __str__(self):
        return u"{0}({1})".format(self.examlesson, self.examFile)
