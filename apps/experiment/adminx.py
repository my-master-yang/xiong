# _*_ encoding:utf-8 _*_
__author__ = "kusole"
__date__ = "17-12-7 下午1:39"

import xadmin

from .models import LabCategory, Lab


class LabCategoryAdmin(object):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class LabAdmin(object):
    list_display = [
        'id', 'labcategory', 'name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image', 'add_time'
    ]
    search_fields = ['labcategory', 'name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image']
    list_filter = [
        'labcategory__name', 'name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image', 'add_time'
    ]


xadmin.site.register(LabCategory, LabCategoryAdmin)
xadmin.site.register(Lab, LabAdmin)
