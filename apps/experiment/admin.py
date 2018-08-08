from django.contrib import admin

# Register your models here.
from .models import Lab, LabCategory


class LabCategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'desc', 'add_time']
    search_fields = ['name', 'desc']
    list_filter = ['name', 'desc', 'add_time']


class LabAdmin(admin.ModelAdmin):
    list_display = ['labcategory', 'name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image', 'add_time']
    search_fields = ['labcategory', 'name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image']
    list_filter = [
        'labcategory__name', 'name', 'desc', 'detail', 'degree', 'learn_times', 'students', 'image', 'add_time'
    ]


admin.site.register(LabCategory, LabCategoryAdmin)
admin.site.register(Lab, LabAdmin)
