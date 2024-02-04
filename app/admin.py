# 这段代码是用于在Django的admin后台注册模型，以便在后台管理界面中对这些模型进行管理。
# 首先，导入了需要注册的模型，包括UserInfo、UserType、ClassInfo、Attendence、Notice、Leave、Exam和ExamContent。
from django.contrib import admin
from .models import UserInfo, UserType, ClassInfo,  Attendence, Notice, Leave, Exam, ExamContent


# Register your models here.

# 然后，定义了一系列Admin类，每个类都指定了要在后台显示的字段。
class UserInfoAdmin(admin.ModelAdmin):
    list_display = ['studentNum', 'username',  'cid', 'password',
                     'gender',  'phone', 'email',
                    ]


class UserTypeAdmin(admin.ModelAdmin):
    list_display = ['id', 'caption']


class ClassInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name']


class MajorInfoAdmin(admin.ModelAdmin):
    list_display = ['id', 'name', ]


class AttendenceAdmin(admin.ModelAdmin):
    list_display = ['id', 'stu', 'date', 'start_time', 'end_time', 'is_leave', 'duration', 'detail']


class NoticeAdmin(admin.ModelAdmin):
    list_display = ['id', 'author', 'head', 'content', 'level']


class LeaveAdmin(admin.ModelAdmin):
    list_display = ['id', 'start_time', 'end_time', 'explain']


class ExamAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'content', 'point', 'detail']


class ExamContentAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'date', 'state']

# 接下来，通过调用admin.site.register()
# 方法，将每个模型和对应的Admin类进行注册。
admin.site.register(UserType, UserTypeAdmin)
admin.site.register(UserInfo, UserInfoAdmin)
admin.site.register(ClassInfo, ClassInfoAdmin)
admin.site.register(Attendence, AttendenceAdmin)
admin.site.register(Notice, NoticeAdmin)
admin.site.register(Leave, LeaveAdmin)
admin.site.register(ExamContent, ExamContentAdmin)
admin.site.register(Exam, ExamAdmin)

#
# 最后，将注册的模型和Admin类添加到Django的admin后台中。
#
# 这样，我们就可以在admin后台中对这些模型进行增删改查操作