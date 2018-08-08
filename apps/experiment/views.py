# Create your views here.
import json

import markdown
from django import shortcuts
from django.core.paginator import Paginator
from django.http import HttpResponse
from django.core.cache import cache
from django.views.generic.base import View

import markdown
import json

from openstack_netsec.models import InstanceList
from openstack_netsec.views import instancevnc
from users.models import LabCollection
from .models import Lab, LabCategory
from .exp_sched.exp_scheduler import exp_scheduler

# 启用实验调度器
if not exp_scheduler.is_alive():
    exp_scheduler.start()


def experimentlab(request, pk, instance_id):
    lab = shortcuts.get_object_or_404(Lab, pk=pk)
    labcategory = lab.labcategory.name
    lab.detail = markdown.markdown(
        lab.detail,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    vnclinking = instancevnc(request, instance_id)
    instancelive = InstanceList.objects.filter(username=request.user.username)
    last_time = 2400
    return shortcuts.render(
        request,
        'experiment_lab.html',
        context={
            'lab': lab,
            'labcategory': labcategory,
            'vnclinking': vnclinking,
            'instancelive': instancelive,
            'last_time': last_time
        })


def experimentlabdetail(request, pk):
    lab = shortcuts.get_object_or_404(Lab, pk=pk)
    labcategory = lab.labcategory.name
    lab.detail = markdown.markdown(
        lab.detail,
        extensions=[
            'markdown.extensions.extra',
            'markdown.extensions.codehilite',
            'markdown.extensions.toc',
        ])
    # vnclinking = instancevnc(request, instance_id)
    # instancelive = InstanceList.objects.filter(username=request.user.username)
    return shortcuts.render(request, 'experimentdetail.html', context={'lab': lab, 'labcategory': labcategory})


def checkinstancelive():
    instancelive = InstanceList.objects.all()
    if instancelive is not None:
        return instancelive
    else:
        return False


# class ExperimentLabView(View):
#     def get(self, request):
#         request_test = request.GET.get("sdr",'')
#         return sss


class ExperimentIndexView(View):
    """
    实验管理列表功能
    """

    experiment_levels = {"cj": "初级", "zj": "中级", "gj": "高级"}

    def get(self, request):
        """
        获取实验列表
        :param request:
        :return:
        """
        labcategory_id = request.GET.get('lcid', '')
        lab_degree = request.GET.get('lablevel', 'all')

        labcategory = LabCategory.objects.all()
        labs = Lab.objects.all()

        if labcategory_id != '':
            # 如果有实验类别id,则返回这个类别下的所有实验
            labs = Lab.objects.all().filter(labcategory_id=labcategory_id)

        if lab_degree != 'all':
            # 通过难度等级对实验进行筛选
            labs = labs.filter(degree=str(lab_degree))


        # 分页
        paginator = Paginator(labs.order_by("id"), 12)
        page = request.GET.get('page', 1)
        labs = paginator.page(page)

        # 判断实验是否被当前用户收藏，使用缓存加速
        cache_key = '{}_collected_labs'.format(request.user.username)
        if cache_key not in cache:
            cache.set(
                cache_key,
                set([item.labpk for item in LabCollection.objects.filter(username=request.user.username)]))
        for lab in labs:
            if lab.id in cache.get(cache_key):
                lab.collected = 1
            else:
                lab.collected = 0

        # 展示正在进行的实验和使能按钮
        instancelive = InstanceList.objects.filter(username=request.user.username)
        buttonlive = "show"
        if instancelive.exists():
            buttonlive = "no-show"

        return shortcuts.render(
            request, 'my_experiment.html', {
                "labcategory_id": labcategory_id,
                "labcategory": labcategory,
                "lab": labs,
                "lab_level": lab_degree,
                "buttonlive": buttonlive,
                "instancelive": instancelive,
            })

    # # 收藏功能接受的ajax post方法
    # def post(self, request):
    #     # labitem_name = request.POST.get('labnamejson')
    #     # labcollectionobj = LabCollection.objects.all()
    #     # labitem_pk = request.POST.get('labpkjson')
    #     # labitempk = int(eval(labitem_pk))
    #     # for obj in labcollectionobj:
    #     #     if obj.labpk == labitempk and obj.username == request.user.username:
    #     #         status = 1
    #     #         return HttpResponse(json.dumps({'status': status}))
    #     # labcollection = LabCollection()
    #     # labcollection.username = request.user.username
    #     # labcollection.labpk = labitempk
    #     # labcollection.name = Lab.objects.get(pk=labcollection.labpk).name
    #     # labcollection.level = Lab.objects.get(pk=labcollection.labpk).degree
    #     # if (labcollection.level == 'cj'):
    #     #     labcollection.level = '初级'
    #     # elif (labcollection.level == 'zj'):
    #     #     labcollection.level = '中级'
    #     # elif (labcollection.level == 'gj'):
    #     #     labcollection.level = '高级'
    #     # labcollection.save()
    #     # status = 0
    #     # return HttpResponse(json.dumps({'status': status}))
    #
    #     lab_item_pk = int(eval(request.POST.get('labpkjson')))
    #
    #     try:
    #         # 已经收藏则取消收藏
    #         lab_collection = LabCollection.objects.get(labpk=lab_item_pk, username=request.user.username)
    #         lab_collection.delete()
    #         status = 1
    #     except LabCollection.DoesNotExist:
    #         # 未收藏则添加收藏
    #         lab_collection = LabCollection()
    #         lab_collection.username = request.user.username
    #         lab_collection.labpk = lab_item_pk
    #         lab_collection.name = Lab.objects.get(pk=lab_collection.labpk).name
    #         lab_collection.level = Lab.objects.get(pk=lab_collection.labpk).degree
    #         lab_collection.level = ExperimentIndexView.experiment_levels.get(lab_collection.level, "初级")
    #         lab_collection.save()
    #         status = 0
    #     return HttpResponse(json.dumps({'status': status}))


class LabCollectionView(View):
    """
    实验收藏
    """

    def get(self, request):
        """
        获取所有已收藏lesson的id
        :param request:
        :return:
        """
        cache_key = '{}_collected_labs'.format(request.user.username)
        if cache_key not in cache:
            labs = [item.labpk for item in LabCollection.objects.filter(username=request.user.username)]
        else:
            labs = cache.get(cache_key)
        labs.sort()
        return HttpResponse(json.dumps(labs))

    def post(self, request):
        """
        添加或者取消收藏
        :param request:
        :return:
        """
        lab_item_pk = int(eval(request.POST.get('labpkjson')))

        try:
            # 已经收藏则取消收藏
            lab_collection = LabCollection.objects.get(labpk=lab_item_pk, username=request.user.username)
            lab_collection.delete()
            status = 1
        except LabCollection.DoesNotExist:
            # 未收藏则添加收藏
            lab_collection = LabCollection()
            lab_collection.username = request.user.username
            lab_collection.labpk = lab_item_pk
            lab_collection.name = Lab.objects.get(pk=lab_collection.labpk).name
            lab_collection.level = Lab.objects.get(pk=lab_collection.labpk).degree
            lab_collection.level = ExperimentIndexView.experiment_levels.get(lab_collection.level, "初级")
            lab_collection.save()
            status = 0

        # 更新缓存
        cache_key = '{}_collected_labs'.format(request.user.username)
        cache.set(
            cache_key,
            set([item.labpk for item in LabCollection.objects.filter(username=request.user.username)]))
        return HttpResponse(json.dumps({'status': status}))