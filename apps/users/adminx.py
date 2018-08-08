# _*_ encoding:utf-8 _*_
__author__ = "kusole"
__date__ = "17-12-1 下午2:14"

import xadmin
from xadmin import views

from .models import UserExamination, LabCollection, LessonCollection, Personal_info


class GlobalSetting(object):
    site_title = u"安捷光通安全培训系统后台管理平台"
    site_footer = u"2017安捷光通成都科技有限公司"
    # menu_style = "accordion"


class BaseSetting(object):
    enable_themes = False
    use_bootswatch = False


class UserExamAdmin(object):
    list_display = ['username', 'examlesson', 'score', 'exam_times']
    search_fields = ['username', 'examlesson']
    list_filter = ['username', 'examlesson', 'score', 'exam_times']


class LabCollectAdmin(object):
    list_display = ['username', 'labpk', 'name', 'level']
    search_fields = ['username', 'name', 'level']
    list_filter = ['username', 'name', 'level']


class LessonCollectAdmin(object):
    list_display = ['username', 'coursepk', 'name', 'level']
    search_fields = ['username', 'name', 'level']
    list_filter = ['username', 'name', 'level']


class Personal_info_Admin(object):
    list_display = ['username', 'nick_name', 'birthday', 'gender', 'mobile', 'qq_number', 'email']
    search_fields = ['username', 'nick_name', 'mobile', 'qq_number', 'email']
    list_filter = ['username', 'nick_name', 'gender', 'mobile', 'qq_number', 'email']


xadmin.site.register(views.CommAdminView, GlobalSetting)
xadmin.site.register(views.BaseAdminView, BaseSetting)
xadmin.site.register(UserExamination, UserExamAdmin)
xadmin.site.register(LabCollection, LabCollectAdmin)
xadmin.site.register(LessonCollection, LessonCollectAdmin)
xadmin.site.register(Personal_info, Personal_info_Admin)
