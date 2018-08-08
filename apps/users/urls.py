__authon__ = 'geyu'
__date__ = '17-12-27 '

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import UserExamView

urlpatterns = [
    url(r'^usercenter/$', login_required(UserExamView.as_view()), name='usercenter'),
]
