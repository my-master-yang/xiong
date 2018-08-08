from django.conf.urls import url
from . import views
from .views import MyExamIndexView, ExamPaperView
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^myexam/$', login_required(MyExamIndexView.as_view()), name='myexam'),
    url(r'^exampage/(?P<exampaper_id>[0-9]+)', login_required(ExamPaperView.as_view()), name='ExamPage'),
]
