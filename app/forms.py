from django import forms
from .models import UserInfo
class loginForm(forms.Form):
    password=forms.CharField(widget=forms.PasswordInput)
    class Meta:
        model=UserInfo
        field=('studentNum')
# 这段代码是一个Django表单的定义。它定义了一个名为loginForm的表单类，用于用户登录功能。
#
# 代码的第一行导入了forms模块和UserInfo模型。forms模块是Django中用于创建表单的模块，而UserInfo是一个自定义的模型类，用于表示用户信息。
#
# 接下来的代码定义了一个loginForm类，继承自forms.Form。这意味着loginForm是一个Django表单类，用于处理用户登录表单的数据。
#
# 在loginForm类中，有一个password字段，它使用了forms.CharField，并指定了widget=forms.PasswordInput。这意味着password字段是一个字符型字段，并且在表单中以密码输入框的形式显示。
#
# 在类的内部，还定义了一个Meta类。这个Meta类用于指定表单的元数据，其中model属性指定了表单的模型为UserInfo，fields属性指定了表单要显示的字段为'studentNum'。
#
# 总结：这段代码定义了一个名为loginForm的Django表单类，用于用户登录功能。表单包含一个密码字段，并指定了要显示的字段为'studentNum'。