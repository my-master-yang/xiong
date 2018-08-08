# _*_ encoding:utf-8 _*_
__author__ = "kusole"
__date__ = "17-12-5 下午7:48"

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import CourseView, LessonView, LessonCollectionView

urlpatterns = [
    url(r'^list/$', login_required(CourseView.as_view()), name='list'),
    url(r'^lesson/(?P<pk>[0-9]+)', login_required(LessonView.as_view()), name='lesson'),
    url(r'^collection/$', login_required(LessonCollectionView.as_view()), name='collection')
]
