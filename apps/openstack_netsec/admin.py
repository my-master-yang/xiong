from django.contrib import admin
# Register your models here.
from .models import InstanceList


class InstanceListAdmin(admin.ModelAdmin):
    list_display = ['name', 'instanceID', 'labID', 'instanceST', 'add_time']
    search_fields = ['name', 'instanceID', 'labID', 'instanceST']
    list_filter = ['name', 'instanceID', 'labID', 'instanceST', 'add_time']


admin.site.register(InstanceList, InstanceListAdmin)
