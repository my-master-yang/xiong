__authon__ = 'geyu'
__date__ = '17-12-11 '

import xadmin

from .models import ExamLesson, ExamCategory, ExamPaper, Question
from .utils import import_examFile


class ExamCategoryAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class ExamLessonAdmin(object):
    list_display = ['id', 'examcategory', 'name', 'desc', 'degree', 'exam_times', 'students', 'image', 'add_time']
    search_fields = ['id', 'examcategory', 'name', 'desc', 'degree', 'exam_times', 'students', 'image']
    list_filter = ['id', 'examcategory__name', 'name', 'desc', 'degree', 'exam_times', 'students', 'image', 'add_time']


class QuestionAdmin(object):
    list_display = [
        'examcategory', 'examLessonNum', 'questionType', 'score', 'content', 'answer', 'OptionA', 'OptionB', 'OptionC',
        'OptionD', 'boolt', 'boolf', 'add_time'
    ]
    search_fields = [
        'examcategory', 'questionType', 'score', 'content', 'answer', 'OptionA', 'OptionB', 'OptionC', 'OptionD',
        'boolt', 'boolf'
    ]
    list_filter = [
        'examcategory', 'examLessonNum', 'questionType', 'score', 'content', 'answer', 'OptionA', 'OptionB', 'OptionC',
        'OptionD', 'boolt', 'boolf', 'add_time'
    ]


class ExamPaperAdmin(object):
    list_display = ['examcategory', 'examlesson', 'examLessonNum', 'examFile', 'add_time']
    search_fields = [
        'examcategory__name', 'examlesson__name', 'examlesson__id', 'question__id', 'question__content',
        'question__answer'
    ]
    list_filter = [
        'examcategory',
        'examlesson',
        'examLessonNum',
        'add_time',
        'examlesson__name',
    ]

    def save_model(self):
        obj = self.new_obj
        re = super(ExamPaperAdmin, self).save_model()
        import_examFile(self, obj)
        return re


xadmin.site.register(ExamCategory, ExamCategoryAdmin)
xadmin.site.register(ExamLesson, ExamLessonAdmin)
xadmin.site.register(Question, QuestionAdmin)
xadmin.site.register(ExamPaper, ExamPaperAdmin)
