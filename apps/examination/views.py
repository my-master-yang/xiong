import json

from django import shortcuts
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.shortcuts import render
from django.views.generic.base import View

from openstack_netsec.models import InstanceList
from users.models import UserExamination
from .models import ExamCategory, ExamLesson, ExamPaper, Question,AnswerCard
from datetime import datetime, timedelta
import time

class MyExamIndexView(View):
    """
    按照考试课程id来查找考试科目
    """

    def get(self, request):
        examcategory_id = request.GET.get('ecid', '')
        if examcategory_id == '':
            examcategory_id = str(ExamCategory.objects.all()[0].id)
        exam_categories = ExamCategory.objects.all()
        exam_subjects = []
        if examcategory_id:
            exam_subjects = ExamLesson.objects.all().filter(examcategory_id=int(examcategory_id))

        exam_subject_level = request.GET.get('examlessonlevel', 'all')

        if exam_subject_level != 'all':
            exam_subjects = ExamLesson.objects.filter(
                examcategory_id=int(examcategory_id), degree=str(exam_subject_level))

        paginator = Paginator(exam_subjects.order_by("id"), 3)
        page = request.GET.get('page')

        try:
            exam_subjects = paginator.page(page)
        except PageNotAnInteger:
            exam_subjects = paginator.page(1)
        except EmptyPage:
            exam_subjects = paginator.page(paginator.num_pages)

        # 展示正在进行的实验和使能按钮
        instancelive = InstanceList.objects.filter(username=request.user.username)
        buttonlive = "show"
        if instancelive.exists():
            buttonlive = "no-show"

        return shortcuts.render(
            request, 'my_exam.html', {
                "examcategory_id": examcategory_id,
                "examcategory": exam_categories,
                "examlesson": exam_subjects,
                "examlesson_level": exam_subject_level,
                "buttonlive": buttonlive,
                "instancelive": instancelive,
            })

    def post(self, request):
        examination_id = request.POST['examination_id']
        cur_number = ExamLesson.objects.get(id=int(examination_id)).students
        cur_number = cur_number + 1
        print("cur=", examination_id)
        print( ExamLesson.objects.filter(id=examination_id))
        ExamLesson.objects.filter(id=examination_id).update(students=cur_number)


class ExamPaperView(View):
    """
    由考试科目的id来删选所属的该科目的所有试题
    """

    def get(self, request, exampaper_id):
        examlesson = ExamLesson.objects.get(id=exampaper_id).name  # 考试科目
        exam_times = ExamLesson.objects.get(id=exampaper_id).exam_times  #科目考试时间
        examlesson_list_id = ExamLesson.objects.filter(id=exampaper_id)  #找到目标考试科目
        examNum = ExamPaper.objects.get(examlesson=examlesson_list_id).examLessonNum  #通过考试科目在试题列表中找到考试试题编号

        # exampapers = ExamPaper.objects.filter(examlesson__id=examlesson_list_id) #找到所有试题
        questions = Question.objects.filter(examLessonNum=int(examNum))  #根据试卷编号筛选题
        question_list = []
        question_id_list = []

        AnswerCard.objects.get_or_create(user_name=request.user.username,number_id=examNum)
        frist_time = AnswerCard.objects.filter(user_name=request.user.username, number_id=examNum)[0].start_time
        #AnswerCard.objects.filter(user_name=request.user.username).delete()
        print("a", frist_time.strftime('%Y-%m-%d %H:%M:%S %f'))#字符串格式化（可进行int等格式话）
        print((int(frist_time.strftime('%Y')))*10)

        now1 = datetime.now().replace(tzinfo=None) #将datetime类转换为timedelta类
        frist_time = frist_time.replace(tzinfo=None)
      #  print("now1=", now1)
        cz=now1-frist_time
        #print("cz=",cz.seconds)
        if (cz>timedelta(seconds=30)): #不在考试区间，创建
            AnswerCard.objects.filter(user_name=request.user.username,number_id=examNum).update(start_time=datetime.now()+timedelta(hours=8))#加了8小时与中国时区相符（主要是数据库的时间没配好设置了也没生效）
        if(cz<timedelta(seconds=30)):  #在考试区间
            print("frist",frist_time)
       # if AnswerCard.objects.get(user_name==request.user.username, number_id=examNum).start_time:
            frist_time = AnswerCard.objects.get(user_name=request.user.username, number_id=examNum).start_time
            print("now",now1)

        for question in questions:
            # question = Question.objects.get(pk=exampaper.question_id)
            question_list.append(question)
            question_id_list.append(question.id)
        title = examlesson
        question_now = tuple(question_list)  #题目元组
        question_count = len(question_now)

        return render(
            request, "exampage.html", {
                "question": question_now,
                "question_count": question_count,
                "title": title,
                "exam_times": json.dumps(exam_times)
            })

    def post(self, request, exampaper_id):
        examlesson = ExamLesson.objects.get(id=exampaper_id).name  # 考试科目
        exam_times = ExamLesson.objects.get(id=exampaper_id).exam_times  # 科目考试时间
        examlesson_list_id = ExamLesson.objects.filter(id=exampaper_id)  # 找到目标考试科目
        # exampapers = ExamPaper.objects.filter(examlesson__id=examlesson_list_id)  # 找到所有试题
        examNum = ExamPaper.objects.get(examlesson=examlesson_list_id).examLessonNum  # 通过考试科目在试题列表中找到考试试题编号
        questions = Question.objects.filter(examLessonNum=int(examNum))  # 根据试卷编号筛选题

        question_list = []
        question_id_list = []
        for question in questions:
            # question = Question.objects.get(pk=exampaper.question_id)
            question_list.append(question)
            question_id_list.append(question.id)
        title = examlesson
        #计算总得分
        temp_score = 0
        print("QusIDList:---", question_id_list)
        for i in question_id_list:
            # print("IIII",i)
            user_answer = request.POST.get(str(i), "")
            # print(user_answer)
            curr_quesiton = Question.objects.get(pk=i)
            if curr_quesiton.answer == user_answer:
                temp_score += curr_quesiton.score
        total_score = temp_score
        # 保存到UserExamination模板里面  判断这个用户这个枯木考没考过　　如果考过则分数更新　　没有则创建
        username = request.user.username
        examlesson = ExamLesson.objects.get(pk=exampaper_id)
        # exam_times = exampaper.examlesson.exam_times
        available_times = request.POST.get('available_times', '')
        print("UUUUsssssTTt", available_times)
        used_times = self.GetExamUsedTimes(exam_times, available_times)
        print("USED_TIMES==", used_times)
        if (UserExamination.objects.filter(username=username, examlesson=examlesson).first() == None):
            UserExamination.objects.create(
                username=username, examlesson=examlesson, score=total_score, exam_times=exam_times)
        else:
            UserExamination.objects.filter(username=username, examlesson=examlesson).update(score=total_score)
        return render(request, "score.html", {
            "score": total_score,
            "title": title,
            "used_timesm": used_times[0],
            "used_timess": used_times[1]
        })

    def GetExamUsedTimes(self, ExamTimes, AvaTimes):
        usedtime = []

        str = AvaTimes.split(":")
        print(str)

        if (str[1] == 0):
            minutes = ExamTimes - int(str[0])
            seconds = 0
        else:
            minutes = ExamTimes - int(str[0]) - 1
            seconds = 60 - int(str[1])

        print(minutes)
        print(seconds)

        # if(minutes < 10 or seconds < 10):
        #     minutes = "%s%d" % ('0',minutes)
        #     seconds = "%s%d" % ('0',seconds)
        #     usedtime = minutes+':'+seconds
        # else:
        #     usedtime = "%d%s%d"%(minutes,':',seconds)

        usedtime.append(minutes)
        usedtime.append(seconds)

        return usedtime
