import sched
import time
from datetime import timedelta
from multiprocessing import Process
from collections import deque

import django.utils.timezone as timezone
import requests

from openstack_netsec.models import InstanceList


class ExpScheduler(Process):
    """
    实验调度员
    """

    def __new__(cls, *args, **kwargs):
        # 单例
        if not hasattr(cls, '_instance'):
            cls._instance = super(ExpScheduler, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        Process.__init__(self)
        self.scheduler = sched.scheduler(time.time, time.sleep)
        self.interval = 300

    def check(self):
        """
        检查是否存在超过时间的实验环境，如果有，就关闭它
        """
        instances = InstanceList.objects.all()
        queue = deque()
        for instance in instances:
            if timezone.now() > instance.add_time + timedelta(hours=1):
                print('实例<{}:{}>已经超时'.format(instance.pk, instance.name))
                queue.append(instance.pk)
        while len(queue) > 0:
            instance_pk = queue.popleft()
            with requests.Session() as sess:
                sess.get('http://127.0.0.1:8000/auth/login/')
                csrftoken = sess.cookies.get('csrftoken', '')
                sess.headers.update({'X-CSRFtoken': csrftoken})
                sess.post('http://127.0.0.1:8000/auth/login/', data={'username': 'admin', 'password': 'anjie888admin'})
                csrftoken = sess.cookies.get('csrftoken', '')
                sess.headers.update({'X-CSRFtoken': csrftoken})
                sess.post('http://127.0.0.1:8000/instance/deletelab/', data={'lab_pk': instance_pk})
        self.scheduler.enter(self.interval, 1, self.check)

    def run(self):
        # 每隔interval秒执行一次检查
        self.scheduler.enter(self.interval, 1, self.check)
        try:
            self.scheduler.run()
        except KeyboardInterrupt:
            pass


exp_scheduler = ExpScheduler()
