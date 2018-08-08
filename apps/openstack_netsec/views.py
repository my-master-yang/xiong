import json
import logging
import os
import time

import django.views.decorators.vary
import futurist
import yaml
from django import shortcuts
from django.conf import settings
from django.core.urlresolvers import reverse
from django.http import HttpResponse
from django.shortcuts import render
from django.utils.text import normalize_newlines
from django.views.generic.base import View

import openstack_netsec.images.utils as image_utils
import openstack_netsec.utils as instance_utils
from experiment.models import Lab
from openstack_netsec import api
from openstack_netsec.horizon import exceptions
from openstack_netsec.instances import console as project_console
from .models import InstanceList

LOG = logging.getLogger(__name__)

# Create your views here.


@django.views.decorators.vary.vary_on_cookie
def splash(request):
    if not request.user.is_authenticated():
        return shortcuts.redirect('/auth/login')
    # try:
    #     instances, more = api.nova.server_list(request, search_opts=None)
    # except Exception:
    #     return

    # for instance in instances:
    #     print(instance.id)
    #     api.nova.server_delete(request ,instance.id)
    # count = 0
    # for instance in instances:
    #     if instance.name.split('_')[-2] == request.user.username:
    #         count = count + 1
    #
    # if count > 2:
    #     # 删除所有实例，清空数据表
    #     try:
    #         for instance in instances:
    #             api.nova.server_delete(request, instance.id)
    #     except Exception as e:
    #         print(e)
    #     InstanceList.objects.filter(username=request.user.username).delete()
    #
    # # if len(instances) > 2:
    # # 删除所有实例，清空数据表
    # # try:
    # #     for instance in instances:
    # #         # print(instance.id)
    # #         api.nova.server_delete(request, instance.id)
    # # except Exception:
    # #     pass
    # # InstanceList.objects.filter(username=request.user.username).delete()
    #
    # elif len(instances) == 0:
    #     # 清空数据表
    #     InstanceList.objects.filter(username=request.user.username).delete()
    #
    # else:
    #     # 取实例并存入数据库
    #     InstanceList.objects.filter(username=request.user.username).delete()
    #     for instance in instances:
    #         if instance.name.split('_')[-2] == request.user.username:
    #             instancelist = InstanceList()
    #             instancelist.instanceID = instance.id
    #             instancelist.name = instance.name
    #             instancelist.username = request.user.username
    #             instancelist.instanceST = instance.status
    #             instancelist.labID = int(instance.name.split('_')[-1])
    #             instancelist.labName = Lab.objects.filter(pk=instancelist.labID)[0].name
    #             instancelist.save()

    response = shortcuts.redirect('/index')
    if 'logout_reason' in request.COOKIES:
        response.delete_cookie('logout_reason')
    if 'logout_status' in request.COOKIES:
        response.delete_cookie('logout_status')
    return response


class IndexView(View):
    def get(self, request):
        # if request.user.is_authenticated():
        #     return render(request, 'listinstance.html')
        return render(request, 'index.html')


class ListInstanceView(View):
    """
    显示实例信息
    """

    def get(self, request):
        instances = []
        flavors = []
        full_flavors = {}
        images = []
        image_map = {}

        def _task_get_instances():
            try:
                tmp_instances, more = api.nova.server_list(self.request, search_opts=None)
            except Exception:
                return

            instances.extend(tmp_instances)

            try:
                api.network.servers_update_addresses(self.request, instances)
            except Exception:
                pass

        def _task_get_flavors():
            try:
                tmp_flavors = api.nova.flavor_list(self.request)
                flavors.extend(tmp_flavors)
                full_flavors.update([str(flavor.id), flavor] for flavor in flavors)
            except Exception:
                pass

        def _task_get_images():
            try:
                tmp_images = api.glance.image_list_detailed(self.request)[0]
                images.extend(tmp_images)
                image_map.update([(str(image.id), image) for image in images])
            except Exception:
                pass

        with futurist.ThreadPoolExecutor(max_workers=3) as e:
            e.submit(fn=_task_get_flavors)
            e.submit(fn=_task_get_images)

        _task_get_instances()

        for instance in instances:
            if hasattr(instance, 'image'):
                if isinstance(instance.image, dict):
                    if instance.image.get('id') in image_map:
                        instance.image = image_map[instance.image.get('id')]
                    else:
                        instance.image['name'] = "-"

            flavor_id = instance.flavor["id"]
            if flavor_id in full_flavors:
                instance.full_flavor = full_flavors[flavor_id]
            else:
                msg = ('Unable to retrieve flavor "%s" for instance "%s".' % (flavor_id, instance.id))
                LOG.info(msg)

        return render(request, 'listinstance.html', {"instances": instances})


def instancevnc(request, instance_id):
    try:
        instance = api.nova.server_get(request, instance_id)
        console_url = project_console.get_console(request, 'SPICE', instance)[1]
        # d = {}
        # d["status"] = "success"
        # d["console_url"] = console_url
        # s = json.dumps(d)
        # return HttpResponse(s, content_type='application/json')
        return console_url
    except Exception:
        redirect = reverse("openstack_netsec:listinstance")
        msg = 'Unable to get VNC console for instance "%s".' % instance_id
        exceptions.handle(request, msg, redirect=redirect)


class VncView(View):
    def post(self, request):
        instance_id = request.POST['instance_id']
        try:
            instance = api.nova.server_get(request, instance_id)
            console_url = project_console.get_console(request, 'VNC', instance)[1]
            d = {}
            d["status"] = "success"
            d["console_url"] = console_url
            s = json.dumps(d)
            return HttpResponse(s, content_type='application/json')
        except Exception:
            redirect = reverse("openstack_netsec:listinstance")
            msg = 'Unable to get VNC console for instance "%s".' % instance_id
            exceptions.handle(request, msg, redirect=redirect)


# class InstanceDetailView(View):
#     def post(self,request):
#


class CreateInstanceView(View):
    """
    创建虚拟机视图
    """

    def post(self, request):
        context = {}
        projects = []
        users = []
        instance_para = {}

        def _is_allow():
            """
            查看是否存在虚拟机
            :return:
            """
            try:
                tmp_instances, more = api.nova.server_list(self.request, search_opts=None)
            except Exception:
                return
            # if (len(tmp_instances) > 1):
            #     return False
            return True

        def _task_get_instance_module():
            """
            获取虚拟机模板文件
            :return:
            """
            try:
                instance_module = Lab.objects.get(pk=request.POST['lab_id']).instance_module
                # instance_module = request.POST['instance_module']
                if instance_module == "":
                    instance_module = "cirros"
                filename = instance_module + ".yaml"
                module_path = os.path.abspath(os.path.join(settings.MODULE_FILES_PATH, filename), )
                fp = open(module_path)
                context_tmp = yaml.load(fp)
            except Exception:
                pass
            context.update(context_tmp)

        def _task_get_user_projects():
            """
            获取项目列表和用户信息
            :return: None
            """
            try:
                projects_tmp = [(tenant.id, tenant.name) for tenant in request.user.authorized_tenants]
                users_tmp = [(request.user.id, request.user.username)]
            except Exception:
                pass

            projects.extend(projects_tmp)
            users.extend(users_tmp)

        def _task_get_image_id():
            """
            获取镜像ID
            :return: None
            """
            image_id_tmp = {}
            try:
                image = context.get('image', None)
                imagetype = context.get('imagetype', None)

                if image and imagetype:
                    image_list = image_utils.get_available_images(request, projects[0][0], None)
                    if imagetype == "snapshot":
                        image_list_tmp = [
                            x for x in image_list
                            if x.name == image and x.properties.get("image_type", '') == "snapshot"
                        ]
                    else:
                        image_list_tmp = [x for x in image_list if x.name == image]

                    if image_list_tmp:
                        image_id_tmp['image_id'] = image_list_tmp[0].id
                    else:
                        # 找不到配置文件中的image对应的镜像
                        raise exceptions
                else:
                    # 配置文件中的没有填写image一项
                    raise exceptions
            except Exception:
                # 镜像获取异常
                pass
            instance_para.update(image_id_tmp)

        def _task_get_flavor_list():
            """
            虚拟机硬件配置选择
            :return: None
            """
            flavor_tmp = {}
            try:
                flavor_list = instance_utils.flavor_field_data(request, False)
                flavor_name = context.get('flavor', None)
                if flavor_name is None:
                    # 设置一个默认值，当配置文件中没有flavor时
                    flavor_name = 'm1.small'
                for flavor in flavor_list:
                    if flavor[1] == flavor_name:
                        flavor_tmp['flavor'] = str(flavor[0])
                        break
            except Exception:
                pass
            instance_para.update(flavor_tmp)

        def _task_get_network_id():
            """
            虚拟机网络选择
            :return: None
            """
            network_id_tmp = {}
            try:
                network_list = instance_utils.network_field_data(request)
                network_name = context.get("network_name", None)
                if network_name is not None:
                    nics = [{
                        "net-id": netids[0],
                        "v4-fixed-ip": ""
                    } for netids in network_list if netids[1] in network_name]
                    # 如果找不到配置文件中的网络，设置为none
                    if len(nics) == 0:
                        nics = None
                else:
                    # 配置文件中没有网络的配置
                    nics = None
                network_id_tmp['nics'] = nics
            except Exception:
                pass
            instance_para.update(network_id_tmp)

        def _task_get_security_group_id():
            """
            设置安全组规则
            :return:
            """
            security_group_tmp = {}
            try:
                security_group_id = context.get("security_group_id", None)
                security_group_list = api.neutron.security_group_list(request)
                security_group_list_tmp = [
                    x.get('id') for x in security_group_list if x.name_or_id in security_group_id
                ]
                # 如果查询不到配置文件中的设置，给定默认的设置
                if security_group_list_tmp is None:
                    security_group_list_tmp = [x.get('id') for x in security_group_list if x.name_or_id == "default"]
                security_group_tmp['security_group_id'] = security_group_list_tmp
            except Exception:
                pass
            instance_para.update(security_group_tmp)

        def _task_get_other():
            name_tmp = {}
            count_tmp = {}
            keypare_id_tmp = {}
            dev_mapping_1_tmp = {}
            dev_mapping_2_tmp = {}
            avail_zone_tmp = {}
            admin_pass_tmp = {}
            disk_config_tmp = {}
            config_drive_tmp = {}
            custom_script_tmp = {}
            scheduler_hints_tmp = {}

            nowtime = time.strftime("%y%m%d%H%M%S")

            if context.get('name', None):
                name_tmp[
                    'name'] = context.get('name') + '_' + nowtime + '_' + users[0][1] + '_' + request.POST["lab_id"]
            else:
                name_tmp['name'] = nowtime + '_' + users[0][1] + '_' + request.POST["lab_id"]

            if context.get("count", None):
                count_tmp["count"] = int(context.get("count"))
            else:
                count_tmp["count"] = int(1)

            if context.get("keypair_id", None):
                keypare_id_tmp["keypair_id"] = context.get("keypair_id")
            else:
                keypare_id_tmp["keypair_id"] = ''

            if context.get("dev_mapping_1", None):
                dev_mapping_1_tmp["dev_mapping_1"] = None
            else:
                dev_mapping_1_tmp["dev_mapping_1"] = None

            if context.get("dev_mapping_2", None):
                dev_mapping_2_tmp["dev_mapping_2"] = None
            else:
                dev_mapping_2_tmp["dev_mapping_2"] = None

            if context.get("avail_zone", None):
                avail_zone_tmp["avail_zone"] = context.get("avail_zone")
            else:
                avail_zone_tmp["avail_zone"] = 'nova'

            if context.get("admin_pass", None):
                admin_pass_tmp["admin_pass"] = context.get("admin_pass")
            else:
                admin_pass_tmp["admin_pass"] = ''

            if context.get("disk_config", None):
                disk_config_tmp["disk_config"] = context.get("disk_config")
            else:
                disk_config_tmp["disk_config"] = 'AUTO'

            if context.get("config_drive", None):
                config_drive_tmp["config_drive"] = context.get("config_drive")
            else:
                config_drive_tmp["config_drive"] = False

            if context.get("custom_script", None):
                custom_script_tmp["custom_script"] = context.get("custom_script")
            else:
                custom_script_tmp["custom_script"] = ''

            if context.get("custom_script", None):
                custom_script_tmp["custom_script"] = context.get("custom_script")
            else:
                custom_script_tmp["custom_script"] = ''

            if context.get("scheduler_hints", None):
                scheduler_hints_tmp["scheduler_hints"] = context.get("scheduler_hints")
            else:
                scheduler_hints_tmp["scheduler_hints"] = {}
            instance_para.update(name_tmp)
            instance_para.update(count_tmp)
            instance_para.update(keypare_id_tmp)
            instance_para.update(dev_mapping_1_tmp)
            instance_para.update(dev_mapping_2_tmp)
            instance_para.update(avail_zone_tmp)
            instance_para.update(admin_pass_tmp)
            instance_para.update(disk_config_tmp)
            instance_para.update(config_drive_tmp)
            instance_para.update(custom_script_tmp)
            instance_para.update(scheduler_hints_tmp)

        if _is_allow():

            _task_get_instance_module()
            _task_get_user_projects()
            _task_get_other()

            with futurist.ThreadPoolExecutor(max_workers=5) as e:
                e.submit(fn=_task_get_image_id)
                e.submit(fn=_task_get_flavor_list)
                e.submit(fn=_task_get_network_id)
                e.submit(fn=_task_get_security_group_id)

            try:
                api.nova.server_create(
                    request,
                    name=instance_para['name'],
                    image=instance_para['image_id'],
                    flavor=instance_para['flavor'],
                    key_name=instance_para['keypair_id'],
                    user_data=normalize_newlines(instance_para['custom_script']),
                    security_groups=instance_para['security_group_id'],
                    block_device_mapping=instance_para['dev_mapping_1'],
                    block_device_mapping_v2=instance_para['dev_mapping_2'],
                    nics=instance_para['nics'],
                    availability_zone=instance_para['avail_zone'],
                    instance_count=instance_para['count'],
                    admin_pass=instance_para['admin_pass'],
                    disk_config=instance_para['disk_config'],
                    config_drive=instance_para['config_drive'],
                    scheduler_hints=instance_para['scheduler_hints'],
                    description=None)

            except Exception:
                exceptions.handle(request)

            d = {}
            d["status"] = "success"
            s = json.dumps(d)
            print(s)
            return HttpResponse(s, content_type='application/json')
        else:
            d = {}
            d["status"] = "fail"
            s = json.dumps(d)
            return HttpResponse(s, content_type='application/json')


class DeleteLabView(View):
    def post(self, request):
        lab_pk = request.POST['lab_pk']
        try:
            instance_to_remove = InstanceList.objects.get(pk=lab_pk)
            api.nova.server_delete(request, instance_to_remove.instanceID)
            instance_to_remove.delete()
            return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
        except Exception:
            return HttpResponse(json.dumps({"status": "failed"}), content_type='application/json')
        # instance_id = InstanceList.objects.filter(pk=lab_pk)[0].instanceID
        # InstanceList.objects.filter(pk=lab_pk)[0].delete()
        # try:
        #     api.nova.server_delete(request, instance_id)
        #     # d = {"status": "success"}
        #     # s = json.dumps(d)
        #     return HttpResponse(json.dumps({"status": "success"}), content_type='application/json')
        # except Exception:
        #     return HttpResponse(json.dumps({"status": "failed"}), content_type='application/json')
        # redirect = reverse("instance:listinstance")
        # msg = 'Unable to get VNC console for instance "%s".' % instance_id
        # exceptions.handle(request, msg, redirect=redirect)


class CheckNewInstanceView(View):
    def post(self, request):
        try:
            instances, more = api.nova.server_list(self.request, search_opts=None)
        except Exception:
            return
        print("---More---", more)
        d = {}
        for instance in instances:
            if instance.status == "BUILD":
                d["status"] = "BUILD"
                s = json.dumps(d)
                return HttpResponse(s, content_type='application/json')

        d["status"] = "success"
        d["instance_id"] = instances[0].id
        s = json.dumps(d)

        # 生成虚拟机正常运行，将虚拟机数据存入数据库
        lab_id = request.POST["lab_id"]
        for instance in instances:
            name = instance.name
            if name.split('_')[-1] == lab_id and name.split('_')[-2] == request.user.username:
                instancelist = InstanceList()
                instancelist.instanceID = instance.id
                instancelist.username = request.user.username
                instancelist.name = instance.name
                instancelist.instanceST = instance.status
                instancelist.labID = int(lab_id)
                instancelist.labName = Lab.objects.all().filter(pk=instancelist.labID)[0].name
                instancelist.save()
                break

        print(s)
        return HttpResponse(s, content_type='application/json')
