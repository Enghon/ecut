from django.db import models
from datetime import datetime
from django.utils import timezone

# 这段代码定义了几个Django模型，用于创建数据库表。每个模型都有不同的字段来存储相关信息。
# 这些模型定义了数据库表的结构，可以通过Django的ORM功能来操作数据库。
# Create your models here.
class UserType(models.Model):
    # 用户类型表  字段：用户类型
    caption = models.CharField(max_length=10)

    def __str__(self):
        return self.caption


class ClassInfo(models.Model):
    # 班级信息表  字段:班级名称
    name = models.CharField(max_length=20)

    def __str__(self):
        return self.name





class UserInfo(models.Model):
    # 创建用户模型，学号,密码，班级，姓名,用户类型,电话，姓名,邮件
    studentNum = models.CharField(max_length=15, primary_key=True)
    password = models.CharField(max_length=64)
    username = models.CharField(max_length=15)
    cid = models.ForeignKey('ClassInfo', null=True,on_delete=models.CASCADE)


    user_type = models.ForeignKey(to='UserType',on_delete=models.CASCADE)
    gender = models.IntegerField(default=1)
    phone = models.CharField(max_length=11)

    email = models.EmailField(null=False)

    def __str__(self):
        return self.username

# 签到表设计
class Attendence(models.Model):
    #签到表   字段：用户，签到时间，签退时间，描述   其他是为了方便操作加的字段可不写
    stu = models.ForeignKey('UserInfo',on_delete=models.CASCADE)

    start_time = models.DateTimeField(null=True, blank=True)
    end_time = models.DateTimeField(null=True, blank=True)
    duration = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    date = models.DateField(default=timezone.now)

    is_leave = models.BooleanField(default=False)
    detail = models.TextField(default='无')
    leave_count = models.IntegerField(default=0)

    def __str__(self):
        return self.stu.username


# 通知表设计
class Notice(models.Model):
    # 通知表  字段：发布人,发布日期，发布标题，发布内容，发布级别
    author = models.ForeignKey('UserInfo',on_delete=models.CASCADE)
    post_date = models.DateTimeField(auto_now=True)
    head = models.TextField(max_length=200)
    content = models.TextField(max_length=500)
    level = models.IntegerField(default=0)


# 事项
class Leave(models.Model):
    # 事项表 字段：用户，开始时间，结束时间，请假原因
    user = models.ForeignKey(to='UserInfo',on_delete=models.CASCADE)
    start_time = models.DateField(null=True, blank=True)
    end_time = models.DateField(null=True, blank=True)
    explain = models.TextField(default='无', max_length=500)



# 考核内容
# 考核内容表：标题，名称，批阅状态
class ExamContent(models.Model):
    title = models.TextField(max_length=200)
    date = models.DateField(auto_now=True)
    state = models.BooleanField(default=False)

    def __str__(self):
        return self.title


#  考核成绩表设计
class Exam(models.Model):
    # 考核成绩表  字段： 用户，考核内容，分数，备注
    user = models.ForeignKey('UserInfo',on_delete=models.CASCADE)
    content = models.ForeignKey(to='ExamContent',on_delete=models.CASCADE)
    point = models.DecimalField(max_digits=3, decimal_places=0, default=0)
    detail = models.TextField(max_length=200, default="无")