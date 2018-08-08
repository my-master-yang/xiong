from django.contrib import admin

# Register your models here.
from .models import UserExamination, LessonCollection, LabCollection, Personal_info


#
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['username']
    search_fields = ['username']
    list_filter = ['username']


class UserExamAdmin(admin.ModelAdmin):
    list_display = ['username', 'examlesson', 'score', 'exam_times']
    search_fields = ['username', 'examlesson']
    list_filter = ['username', 'examlesson', 'score', 'exam_times']


class LabCollectAdmin(admin.ModelAdmin):
    list_display = ['username', 'labpk', 'name', 'level']
    search_fields = ['username', 'name', 'level']
    list_filter = ['username', 'name', 'level']


class LessonCollectAdmin(admin.ModelAdmin):
    list_display = ['username', 'coursepk', 'name', 'level']
    search_fields = ['username', 'name', 'level']
    list_filter = ['username', 'name', 'level']


class Personal_info_Admin(admin.ModelAdmin):
    list_display = ['username', 'nick_name', 'birthday', 'gender', 'mobile', 'qq_number', 'email']
    search_fields = ['username', 'nick_name', 'mobile', 'qq_number', 'email']
    list_filter = ['username', 'nick_name', 'gender', 'mobile', 'qq_number', 'email']


admin.site.register(UserExamination, UserExamAdmin)
admin.site.register(LabCollection, LabCollectAdmin)
admin.site.register(LessonCollection, LessonCollectAdmin)
admin.site.register(Personal_info, Personal_info_Admin)
