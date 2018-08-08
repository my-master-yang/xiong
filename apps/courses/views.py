import json

import markdown
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404
from django.views.generic.base import View
from django.core.cache import cache

from openstack_netsec.models import InstanceList
from users.models import LessonCollection
from .models import CourseCategory, Course, Lesson


class CourseView(View):
    """
    课程管理列表功能
    """

    lesson_levels = {'cj': '初级', 'zj': '中级', 'gj': '高级'}

    def get(self, request):
        """
        获取课程列表
        :param request:
        :return:
        """
        course_category_id = request.GET.get('ccid', '')
        course_id = request.GET.get('cid', '')
        lesson_level = request.GET.get('lessonlevel', 'all')

        categories = CourseCategory.objects.all()
        courses = Course.objects.all()
        lessons = Lesson.objects.all()

        if course_id == '':
            # 没有课程id
            if course_category_id != '':
                # 有类别id，则返回这个类别下的所有课程
                courses = courses.filter(coursecategory_id=course_category_id)
                lessons = lessons.filter(coursecategory_id=course_category_id)
        else:
            # 有课程id
            try:
                # 通过课程id获取类别id，并返回相应课程
                course_category_id = str(Course.objects.get(id=course_id).coursecategory_id)
                courses = courses.filter(coursecategory_id=course_category_id)
                lessons = lessons.filter(course_id=course_id)
            except Course.DoesNotExist:
                # 如果课程id对应的课程不存在，返回所有课程
                course_category_id = ''
                course_id = ''

        # 根据难度对lesson进行过滤
        if lesson_level != 'all':
            lessons = lessons.filter(degree=str(lesson_level))

        # 分页
        paginator = Paginator(lessons.order_by("id"), 12)
        page = request.GET.get('page', 1)
        lessons = paginator.page(page)

        # 判断课程是否被当前用户收藏，使用缓存加速
        cache_key = '{}_collected_lessons'.format(request.user.username)
        if cache_key not in cache:
            cache.set(
                cache_key,
                set([item.coursepk for item in LessonCollection.objects.filter(username=request.user.username)]))
        for lesson in lessons:
            if lesson.id in cache.get(cache_key):
                lesson.collected = 1
            else:
                lesson.collected = 0

        # 展示正在进行的实验和使能按钮
        instance_live = InstanceList.objects.filter(username=request.user.username)

        return render(
            request, 'netsec.html', {
                "coursecategory_all": categories,
                "all_course": courses,
                "all_lesson": lessons,
                "coursecategory_id": course_category_id,
                "course_id": course_id,
                "lesson_level": lesson_level,
                "instancelive": instance_live,
            })


class LessonView(View):
    """
    小节
    """

    def get(self, request, pk):
        """
        获取小节的详细内容
        :param request:
        :param pk:
        :return:
        """
        lesson = get_object_or_404(Lesson, pk=pk)
        course_category = lesson.course.coursecategory.name
        course = lesson.course.name
        video_path = '//player.bilibili.com/player.html?aid=24750944&cid=41631714&page=1'
        lesson.detail = markdown.markdown(
            lesson.detail,
            extensions=[
                'markdown.extensions.extra',
                'markdown.extensions.codehilite',
                'markdown.extensions.toc',
            ])
        return render(
            request,
            'course.html',
            context={
                'lesson': lesson,
                'coursecategory': course_category,
                'course': course,
                'video_path': video_path
            })


class LessonCollectionView(View):
    """
    课程收藏
    """

    def get(self, request):
        """
        获取所有已收藏lesson的id
        :param request:
        :return:
        """
        cache_key = '{}_collected_lessons'.format(request.user.username)
        if cache_key not in cache:
            lessons = [item.coursepk for item in LessonCollection.objects.filter(username=request.user.username)]
        else:
            lessons = cache.get(cache_key)
        lessons.sort()
        return HttpResponse(json.dumps(lessons))

    def post(self, request):
        """
        添加或者取消收藏
        :param request:
        :return:
        """
        lesson_item_pk = int(eval(request.POST.get('lessonpkjson')))

        try:
            # 已经收藏则取消收藏
            lesson_collection = LessonCollection.objects.get(coursepk=lesson_item_pk, username=request.user.username)
            lesson_collection.delete()
            status = 1
        except LessonCollection.DoesNotExist:
            # 未收藏则添加收藏
            lesson_collection = LessonCollection()
            lesson_collection.username = request.user.username
            lesson_collection.coursepk = lesson_item_pk
            lesson_collection.name = Lesson.objects.get(pk=lesson_item_pk).name
            lesson_collection.level = Lesson.objects.get(pk=lesson_item_pk).degree
            lesson_collection.level = CourseView.lesson_levels.get(lesson_collection.level, '初级')
            lesson_collection.save()
            status = 0

        # 更新缓存
        cache_key = '{}_collected_lessons'.format(request.user.username)
        cache.set(
            cache_key,
            set([item.coursepk for item in LessonCollection.objects.filter(username=request.user.username)]))
        return HttpResponse(json.dumps({'status': status}))
