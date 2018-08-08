# _*_ encoding:utf-8 _*_
__author__ = "kusole"
__date__ = "17-12-5 下午7:58"

from django.conf.urls import url
from .views import CreateInstanceView, CheckNewInstanceView, DeleteLabView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^createinstance/', login_required(CreateInstanceView.as_view()), name='createinstance'),
    url(r'^checknewinstance/', login_required(CheckNewInstanceView.as_view()), name='checknewinstance'),
    url(r'^deletelab/', login_required(DeleteLabView.as_view()), name='deletelab')
]
