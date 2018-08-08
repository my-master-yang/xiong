"""netsec URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
import xadmin
from django.conf.urls import url, include
from django.contrib import admin
from django.views.static import serve
from openstack_auth import utils

from netsec.settings import MEDIA_ROOT
from openstack_netsec import views
from openstack_netsec.views import IndexView

utils.patch_middleware_get_user()
INSTANCES = r'^(?P<instance_id>[^/]+)/%s$'
from django.contrib.auth.decorators import login_required

urlpatterns = [
    url(r'^$', views.splash, name='splash'),
    url(r'^xadmin/', xadmin.site.urls),
    url(r'^admin/', admin.site.urls),
    url(r'^auth/', include('openstack_auth.urls')),
    url(r'^index/', login_required(IndexView.as_view()), name='index'),

    # 配置上传文件的访问地址
    url(r'^media/(?P<path>.*)$', serve, {"document_root": MEDIA_ROOT}),
    url(r'^course/', include('courses.urls', namespace="course")),
    url(r'^experiment/', include('experiment.urls', namespace="experiment")),
    url(r'^exam/', include('examination.urls', namespace='examination')),
    url(r'^user/', include('users.urls', namespace='users')),
    url(r'^instance/', include('openstack_netsec.urls', namespace='instance'))
]
