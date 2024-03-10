from django.shortcuts import render, HttpResponse, redirect
from .forms import loginForm
from django.contrib.auth import authenticate, login
from .api import check_cookie, check_login, DecimalEncoder, get_all_class, get_all_type, is_login
from .models import UserType, UserInfo, ClassInfo, Attendence, Notice, Leave, ExamContent, Exam
# django自带加密解密库
from django.views.decorators.csrf import csrf_exempt
from django.db.models import F, Q, Avg, Sum, Max, Min, Count
import json
import hashlib
import json
import datetime
import pytz





def introduction(request):
    return render(request,'introduction.html')

def index(request):
    return redirect('/check/')
                                                             # 退出登录
def logout(request):
    req = redirect('/login/')
    req.delete_cookie('asdf')
    req.delete_cookie('qwer')
    return req

                                                            # 登录页面
@csrf_exempt
def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        m1 = hashlib.sha1()
        m1.update(password.encode('utf8'))
        password = m1.hexdigest()
        if check_login(email, password):
            response = redirect('/index/')
            response.set_cookie('qwer', email, 3600)
            response.set_cookie('asdf', password, 3600)
            return response
            #    - 返回重定向对象response。
        else:
            #    - 如果验证失败，将错误信息传递给模板并渲染出登录页面。
            return render(request, 'account/page-login.html', {'error_msg': '账号或密码错误请重新输入'})
    else:
        (flag, rank) = check_cookie(request)
        print('flag', flag)
        if flag:
            return redirect('/index/')
        return render(request, 'account/page-login.html', {'error_msg': ''})


                                                        # 注册页面
@csrf_exempt #@csrf_exempt表示这个视图函数不需要CSRF验证。
def register(request):
    if request.method == 'POST':
        #判断请求是否为Ajax请求。
        if request.is_ajax():
            #获取前端传来的学号。
            stu_num_v = request.POST.get('stu_num_verify')
            #如果该学号已经被注册过，返回False。
            if UserInfo.objects.filter(studentNum=stu_num_v):
                ret = {'valid': False}
                #创建一个字典，包含"valid": False或"valid": True。
            else:
                ret = {'valid': True}
            #将字典转换成JSON格式并返回给前端
            return HttpResponse(json.dumps(ret))

    else:#如果请求不是POST方法或不是Ajax请求，返回渲染后的register.html模板。
        return render(request, 'account/register.html')

                                                            # 签到页面
def check(request):
    (flag, rank) = check_cookie(request)
    user = rank
    if flag:
        if request.method == 'POST':
            sign_flag = request.POST.get('sign')
            print('sign_flag', type(sign_flag), sign_flag)
            if sign_flag == 'True':
                Attendence.objects.create(stu=user, start_time=datetime.datetime.now())
            elif sign_flag == 'False':
                cur_attendent = Attendence.objects.filter(stu=user, end_time=None)
                tmp_time = datetime.datetime.now()
                duration = round((tmp_time - cur_attendent.last().start_time).seconds / 3600, 1)
                cur_attendent.update(end_time=tmp_time, duration=duration)
            return HttpResponse(request, '操作成功')
        else:            # 查询上一个签到的状态
            pre_att = Attendence.objects.filter(stu=user).order_by('id').last()
            if pre_att:# 如果当前时间距上次签到时间超过六小时，并且上次签退时间等于签到时间
                if (datetime.datetime.now() - pre_att.start_time.replace(
                        tzinfo=None)).seconds / 3600 > 6 and pre_att.end_time == None:
                    pre_att.delete()
                    sign_flag = True
                elif (datetime.datetime.now() - pre_att.start_time.replace(
                        tzinfo=None)).seconds / 3600 < 6 and pre_att.end_time == None:
                    sign_flag = False
                else:
                    sign_flag = True
            else:
                sign_flag = True
            if user.user_type.caption =='admin':
                att_list = Attendence.objects.filter(stu__cid=user.cid).order_by('-id')
            else:
                att_list = Attendence.objects.filter(stu=user).order_by('-id')
            return render(request, 'attendance/check.html', locals())
    return render(request, 'account/page-login.html', {'error_msg': ''})


                                                        # 签到统计
@is_login
def total(request):
    (flag, user) = check_cookie(request)
    (flag, rank) = check_cookie(request)
    user = rank
    if rank.user_type.caption == 'admin':
        if request.method == 'POST':
            nowdate = datetime.datetime.now()#    a. 获取当前日期和星期几。
            weekDay = datetime.datetime.weekday(nowdate)
            firstDay = nowdate - datetime.timedelta(days=weekDay)
            lastDay = nowdate + datetime.timedelta(days=6 - weekDay)
            info_list = Attendence.objects.filter(date__gte=firstDay, date__lte=lastDay,stu__cid=user.cid).values( \
                'stu', 'stu__username', 'stu__cid__name', ).annotate(total_time=Sum('duration')).order_by()
            info_list = json.dumps(list(info_list), cls=DecimalEncoder)
            return HttpResponse(info_list)
        else:
            nowdate = datetime.datetime.now()
            weekDay = datetime.datetime.weekday(nowdate)
            firstDay = nowdate - datetime.timedelta(days=weekDay)
            lastDay = nowdate + datetime.timedelta(days=6 - weekDay)
            info_list = Attendence.objects.filter(date__gte=firstDay, date__lte=lastDay,stu__cid=user.cid).values('stu', 'stu__username',
                                                                                          'stu__cid__name').annotate(
                total_time=Sum('duration')).order_by()
            return render(request, 'attendance/total.html', locals())
    else:
        return render(request, 'denied.html')




                                                        # 注册验证
def register_verify(request):
    if request.method == 'POST':
        print('验证成功')
        username = request.POST.get('username')
        email = request.POST.get('email')
        stu_num = request.POST.get('stu_num')
        pwd = request.POST.get('password')

        cid_id = request.POST.get('class')
        m1 = hashlib.sha1()

        m1.update(pwd.encode('utf8'))
        pwd = m1.hexdigest()
        phone = request.POST.get('phone')
        a = UserInfo.objects.create(username=username, email=email,
                                    cid_id=cid_id,
                                    studentNum=stu_num, password=pwd,
                                    phone=phone, user_type_id=2)
        a.save()
        return HttpResponse('OK')


                                                     # 班级管理
def classManage(request):
    (flag, rank) = check_cookie(request)
    print('flag', flag)
    if flag:
        if rank.user_type.caption == 'admin':
            class_list = ClassInfo.objects.all()


            return render(request, 'class/classManage.html', {'class_list': class_list})
        else:
            return render(request, 'denied.html')
    else:
        return render(request, 'account/page-login.html', {'error_msg': ''})

@csrf_exempt
def edit_class(request):
    (flag, rank) = check_cookie(request)
    print('flag', flag)
    if flag:
        if rank.user_type.caption == 'admin':
            if request.method == 'POST':
                pre_edit_id = request.POST.get('edit_id')
                class_name = request.POST.get('edit_class_name')
                temp_flag = ClassInfo.objects.filter(name=class_name)
                print('pre_edit_id1', pre_edit_id)
                pre_obj = ClassInfo.objects.get(id=pre_edit_id)
                if not temp_flag and class_name:
                    pre_obj.name = class_name
                    pre_obj.save()
                return HttpResponse('班级修改成功')
            class_list = ClassInfo.objects.all()
            return render(request, 'class/classManage.html', {'class_list': class_list})
            # return HttpResponse('编辑班级')
        else:
            return render(request, 'denied.html')
    else:
        return render(request, 'account/page-login.html', {'error_msg': ''})



@csrf_exempt
def add_class(request):
    if request.method == 'POST':
        add_class_name = request.POST.get('add_class_name')
        flag = ClassInfo.objects.filter(name=add_class_name)
        if flag:
            return HttpResponse('班级已存在')
            pass

            # print('已有数据，不处理')
        else:
            if add_class_name:
                ClassInfo.objects.create(name=add_class_name).save()
                return HttpResponse('添加成功')

def delete_class(request):
    (flag, rank) = check_cookie(request)
    print('flag', flag)
    if flag:
        if rank.user_type.caption == 'admin':
            delete_id = request.GET.get('delete_id')
            ClassInfo.objects.filter(id=delete_id).delete()
            return redirect('/classManage/')
        else:
            return render(request, 'denied.html')
    else:
        return render(request, 'account/page-login.html', {'error_msg': ''})



# 公告墙展示
@is_login
def notice(request):
    (flag, user) = check_cookie(request)
    user_class = user.cid
    info_list = Notice.objects.filter(author__cid=user_class).order_by('-post_date')
    return render(request, 'notice/notice.html', locals())


# 公告墙发布
@is_login
def noticeManage(request):
    (flag, user) = check_cookie(request)
    if user.user_type.caption == 'admin' or user.user_type.caption == '学生管理员':
        if request.method == 'POST':
            title = request.POST.get('title')
            content = request.POST.get('content')
            level = request.POST.get('selectLevel')
            Notice.objects.create(head=title, content=content, level=level, author=user)
            return render(request, 'notice/notice_manage.html')
        else:
            return render(request, 'notice/notice_manage.html')
    else:
        return render(request, 'denied.html')

                                                    #事项
@is_login
def leave(request):
    (flag, user) = check_cookie(request)
    user_class = user.cid
    leave_list = Leave.objects.filter(user__cid=user_class)

    if request.method == 'POST':
        starttime = request.POST.get('starttime')
        endtime = request.POST.get('endtime')
        print(starttime)
        a = int(datetime.datetime.strptime(starttime, '%Y-%m-%d').day - datetime.datetime.strptime(endtime,'%Y-%m-%d').day) + 1
        explain = request.POST.get('explain')
        Leave.objects.create(start_time=starttime, end_time=endtime, user=user, explain=explain)
    return render(request, 'attendance/leave.html', locals())


# 考核记录
@is_login
def exam(request):
    (flag, user) = check_cookie(request)
    exam_list = ExamContent.objects.all()
    exam_id = request.GET.get('exam_id')
    if exam_id:

        user_list = Exam.objects.filter(content_id=exam_id).all()
        total_point = max(item.point for item in user_list)
        ratio_list = [item.point / total_point for item in user_list]
        total_point1 = max(item.point for item in user_list)-1

        user_list_with_ratio = list(zip(user_list, ratio_list))
    grades = [
        {"name": "优秀(90%-100%)", "color": "#008000", "min_point": 0.89, "max_point": 1.0},
        {"name": "良好(80%-89%)", "color": "#FFA500", "min_point": 0.79, "max_point": 0.89},
        {"name": "及格(60%-79%)", "color": "#FFC125", "min_point": 0.59, "max_point": 0.79},
        {"name": "不及格(0-59%)", "color": "#FF0000", "min_point": 0.00, "max_point": 0.59}
    ]
    return render(request, 'exam/exam.html', locals())


# 考核管理
@is_login
def exam_manage(request):
    (flag, user) = check_cookie(request)
    if user.user_type.caption == 'admin':
        if request.method == 'POST':
            title = request.POST.get('title')

            if title:
                ExamContent.objects.create(title=title)
            else:
                # count = UserInfo.objects.all().count()
                count = UserInfo.objects.filter(cid=user.cid).count()
                content_id = request.POST.get('exam_id')
                for i in range(count):
                    point = request.POST.get('point{}'.format(i))
                    stuID = request.POST.get('stu{}'.format(i))
                    detail = request.POST.get('detail{}'.format(i))
                    Exam.objects.create(point=point, content_id=content_id, user_id=stuID, detail=detail)
                ExamContent.objects.filter(id=content_id).update(state=True)
        check_list = ExamContent.objects.filter(state=False).order_by('-id')
        user_list = UserInfo.objects.filter(cid=user.cid).order_by('studentNum')
        return render(request, 'exam/exam_manage.html', locals())
    else:
        return render(request, 'denied.html')




                                                        # 成员管理
def member_manage(request):
    (flag, rank) = check_cookie(request)
    (flag, user) = check_cookie(request)
    if flag:
        if rank.user_type.caption == 'admin':
            member_list = UserInfo.objects.filter(cid=user.cid)
            return render(request, 'member/member_manage.html', {'member_list': member_list})
        else:
            return render(request, 'denied.html')
    else:
        return render(request, 'account/page-login.html', {'error_msg': ''})


# 删除成员
# 1. 首先，调用 check_cookie 函数，传入 request 参数，并将返回值赋给 (flag, rank) 元组。
# 2. 如果 flag 为真，则进入下一步判断。
# 3. 如果 rank.user_type.caption 的值为'admin'，则获取所有的 UserInfo 对象，并将其赋给 member_list 变量。
# 4. 将 member_list 作为参数传递给 render 函数，渲染 member/member_manage.html 模板，并返回该模板的响应。
# 5. 如果 rank.user_type.caption 的值不为'admin'，则渲染 denied.html 模板，并返回该模板的响应。
# 6. 如果 flag 为假，则渲染 account/page-login.html 模板，并将空字符串作为 error_msg 参数传递给 render 函数，最后返回该模板的响应。
def delete_member(request):
    (flag, rank) = check_cookie(request)
    (flag, user) = check_cookie(request)
    if flag:
        if rank.user_type.caption == 'admin':
            delete_sno = request.GET.get('delete_sno')
            UserInfo.objects.get(studentNum=delete_sno).delete()
            member_list = UserInfo.objects.filter(cid=user.cid)
            return render(request, 'member/member_manage.html', {'member_list': member_list})
        else:
            return render(request, 'denied.html')
    else:
        return render(request, 'account/page-login.html', {'error_msg': ''})


#   编辑成员
def edit_member(request):
    (flag, rank) = check_cookie(request)
    if flag:
        if rank.user_type.caption == 'admin':
            if request.method == 'POST':
                student_num = request.POST.get('student_num')
                username = request.POST.get('username')
                email = request.POST.get('email')
                gender = int(request.POST.get('gender'))
                cls = ClassInfo.objects.get(name=request.POST.get('cls'))
                usertype = UserType.objects.get(caption=request.POST.get('user_type'))
                phone = request.POST.get('phone')
                password = request.POST.get('password')
                edit_obj = UserInfo.objects.filter(studentNum=student_num)
                passq = edit_obj.values('password').first()
                if password==passq['password']:
                    edit_obj.update(studentNum=student_num, username=username,email=email, cid=cls, user_type=usertype, gender=gender, phone=phone,)
                else:
                    a = hashlib.sha1(password.encode("utf-8")).hexdigest()
                    edit_obj.update(studentNum=student_num, username=username,email=email, password=a, cid=cls,user_type=usertype,gender=gender, phone=phone,)
                member_list = UserInfo.objects.all()
                return redirect('/memberManage/', {'member_list': member_list})
            else:
                edit_member_id = request.GET.get('edit_sno')
                stu_type_list = UserType.objects.all()
                cls_list = ClassInfo.objects.all()
                edit_stu_obj = UserInfo.objects.get(studentNum=edit_member_id)
                return render(request, 'member/edit_member.html', locals())
        else:
            return render(request, 'denied.html')
    else:
        return render(request, 'account/page-login.html', {'error_msg': ''})

