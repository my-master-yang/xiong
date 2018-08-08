from django.contrib import admin

# Register your models here.
from .models import ExamLesson, ExamCategory, ExamPaper, Question
from .utils import import_examFile


class ExamCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class ExamLessonAdmin(admin.ModelAdmin):
    list_display = ['examcategory', 'name', 'desc', 'degree', 'exam_times', 'students', 'image', 'add_time']
    search_fields = ['examcategory', 'name', 'desc', 'degree', 'exam_times', 'students', 'image']
    list_filter = ['examcategory__name', 'name', 'desc', 'degree', 'exam_times', 'students', 'image', 'add_time']


class QuestionAdmin(admin.ModelAdmin):
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


class ExamPaperAdmin(admin.ModelAdmin):
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

    def save_model(self, request, obj, form, change):
        re = super(ExamPaperAdmin, self).save_model(request, obj, form, change)
        import_examFile(self, request, obj, change)
        return re


admin.site.register(ExamCategory, ExamCategoryAdmin)
admin.site.register(ExamLesson, ExamLessonAdmin)
admin.site.register(Question, QuestionAdmin)
admin.site.register(ExamPaper, ExamPaperAdmin)
