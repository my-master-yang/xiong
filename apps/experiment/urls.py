# _*_ encoding:utf-8 _*_
__author__ = "kusole"
__date__ = "17-12-5 下午7:58"

from django.conf.urls import url
from django.contrib.auth.decorators import login_required

from .views import ExperimentIndexView, LabCollectionView, experimentlab, experimentlabdetail

INSTANCES = r'^(?P<instance_id>[^/]+)/%s$'

urlpatterns = [
    url(r'^myexperi/$', login_required(ExperimentIndexView.as_view()), name='myexperi'),
    url(r'^experilab/(?P<pk>[0-9]+)/(?P<instance_id>[^/]+)', login_required(experimentlab), name='experilab'),
    url(r'^experilabdetail/(?P<pk>[0-9]+)', login_required(experimentlabdetail), name='experilabdetail'),
    url(r'^collection/$', login_required(LabCollectionView.as_view()), name='collection'),
]
