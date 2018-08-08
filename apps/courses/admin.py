from django.contrib import admin
# Register your models here.
from .models import CourseCategory, Course, Lesson


class CourseCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseAdmin(admin.ModelAdmin):
    list_display = ['coursecategory', 'name', 'add_time']
    search_fields = ['coursecategory', 'name']
    list_filter = ['coursecategory__name', 'name', 'add_time']


# class ChapterAdmin(admin.ModelAdmin):
#     list_display = ['course', 'name', 'add_time']
#     search_fields = ['course', 'name']
#     list_filter = ['course__name', 'name', 'add_time']


class LessonAdmin(admin.ModelAdmin):
    #list_display = ['chapter', 'name', 'desc','detail', 'degree', 'learn_times', 'students', 'image', 'add_time']
    list_display = ['desc', 'detail', 'degree', 'learn_times', 'students', 'image', 'add_time']
    # search_fields = ['chapter', 'name', 'desc', 'detail','degree', 'learn_times', 'students', 'image']
    # list_filter = ['chapter__name', 'name', 'desc', 'detail','degree', 'learn_times', 'students', 'image', 'add_time']


admin.site.register(Lesson, LessonAdmin)
# admin.site.register(Chapter, ChapterAdmin)
admin.site.register(Course, CourseAdmin)
admin.site.register(CourseCategory, CourseCategoryAdmin)
