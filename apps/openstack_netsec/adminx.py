# _*_ encoding:utf-8 _*_
__author__ = "kusole"
__date__ = "17-12-1 下午2:15"

from .models import InstanceList

import xadmin


class InstanceListAdmin(object):
    list_display = ['name', 'instanceID', 'labID', 'instanceST', 'add_time']
    search_fields = ['name', 'instanceID', 'labID', 'instanceST']
    list_filter = ['name', 'instanceID', 'labID', 'instanceST', 'add_time']


xadmin.site.register(InstanceList, InstanceListAdmin)
