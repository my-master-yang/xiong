import json

from django.http import HttpResponse
from django.shortcuts import render
from django.views.generic.base import View

from courses.models import Lesson
from examination.models import ExamLesson
from experiment.models import Lab
from openstack_netsec.models import InstanceList
from .models import UserExamination, LabCollection, LessonCollection, Personal_info


class UserExamView(View):
    """
    按照username删选，得到历史考试内容
    """

    def get(self, request):
        username = request.user.username
        userexam = UserExamination.objects.filter(username=username)
        labcollection = LabCollection.objects.filter(username=username)
        lessoncollection = LessonCollection.objects.filter(username=username)
        personalinfo = Personal_info.objects.filter(username=username).first()
        user_exam_count = len(UserExamination.objects.filter(username=username))
        collected_course_count = len(lessoncollection)
        collected_lab_count = len(labcollection)
        exam_count = len(ExamLesson.objects.all())
        course_count = len(Lesson.objects.all())
        lab_count = len(Lab.objects.all())

        print("request=")

        print(UserExamination.objects.all())
        print(UserExamination.objects.name)
        # 展示正在进行的实验和使能按钮
        instancelive = InstanceList.objects.filter(username=request.user.username)
        buttonlive = "show"
        if instancelive.exists():
            buttonlive = "no-show"

        return render(
            request,
            "user_center.html",
            context={
                "userexams": userexam,
                "labcollection": labcollection,
                "lessoncollection": lessoncollection,
                "user_exam_count": user_exam_count,
                "collected_course_count": collected_course_count,
                "collected_lab_count": collected_lab_count,
                "exam_count": exam_count,
                "course_count": course_count,
                "lab_count": lab_count,
                "buttonlive": buttonlive,
                "instancelive": instancelive,
                "personalinfo": personalinfo,
            })

    def post(self, request):
        username = request.user.username
        name = request.POST['name']
        sex = request.POST['sex']
        birth = request.POST['birth']
        mobile = request.POST['mobile']
        qq_number = request.POST['qqnumber']
        email = request.POST['email']

        clear = request.POST['clear']
        if(clear=='clear_exam'):
           UserExamination.objects.filter(username=username).delete()
        if(clear=='clear_lab'):
            LabCollection.objects.filter(username=username).delete()
        if(clear=='clear_lesson'):
            LessonCollection.objects.filter(username=username).delete()

        print("pusename=",username)
        print("clear=", clear)

        try:
            pi = Personal_info.objects.get(username=username)
            pi.nick_name = name
            pi.gender = sex
            pi.birthday = birth
            pi.mobile = mobile
            pi.qq_number = qq_number
            pi.email = email
            pi.save()
        except Personal_info.DoesNotExist:
            Personal_info.objects.create(
                username=username,
                nick_name=name,
                gender=sex,
                birthday=birth,
                mobile=mobile,
                qq_number=qq_number,
                email=email)

        # if Personal_info.objects.filter(username=username).first() is None:
        #     Personal_info.objects.create(
        #         username=username,
        #         nick_name=name,
        #         gender=sex,
        #         birthday=birth,
        #         mobile=mobile,
        #         qq_number=qqnumber,
        #         email=email)
        # else:
        #     Personal_info.objects.filter(username=username).update(
        #         nick_name=name, gender=sex, birthday=birth, mobile=mobile, qq_number=qqnumber, email=email)
        result = 'sucess'
        return HttpResponse(json.dumps({'result': result}), content_type='application/json')
