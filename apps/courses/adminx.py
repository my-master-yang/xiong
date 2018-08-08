# _*_ encoding:utf-8 _*_
__author__ = "kusole"
__date__ = "17-12-1 下午2:14"

import xadmin

from .models import CourseCategory, Course, Lesson


class CourseCategoryAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class CourseAdmin(object):
    list_display = ['coursecategory', 'name', 'add_time']
    search_fields = ['coursecategory', 'name']
    list_filter = ['coursecategory__name', 'name', 'add_time']


# class ChapterAdmin(object):
#     list_display = ['course', 'name', 'add_time']
#     search_fields = ['course', 'name']
#     list_filter = ['course__name', 'name', 'add_time']


class LessonAdmin(object):
    list_display = ['name', 'desc', 'degree', 'learn_times', 'students', 'image', 'add_time']
    search_fields = ['name', 'desc', 'degree', 'learn_times', 'students', 'image']
    list_filter = ['name', 'desc', 'degree', 'learn_times', 'students', 'image', 'add_time']


xadmin.site.register(Lesson, LessonAdmin)
# xadmin.site.register(Chapter, ChapterAdmin)
xadmin.site.register(Course, CourseAdmin)
xadmin.site.register(CourseCategory, CourseCategoryAdmin)
