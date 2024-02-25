# 这段代码是一个Django应用程序中的一些函数和类的定义。它的主要功能是检查用户是否已登录并进行相应的处理。
# 首先，代码导入了一些模块和类，包括 `UserInfo` 、 `ClassInfo` 和 `UserType` 模型，以及 `wraps` 函数和 `render` 函数。
from .models import UserInfo,ClassInfo,UserType
from functools import wraps
from django.shortcuts import render
import json
import decimal
# 接下来，代码定义了一个名为 `check_cookie` 的函数。该函数检查请求中的cookie是否包含特定的键值对（"qwer"和"asdf"）。
# 如果包含这些键值对，函数会从cookie中获取电子邮件和密码，并使用这些信息查询 `UserInfo` 模型。如果查询结果为空，函数返回(False, -1)，
# 否则返回(True, select_user[0])。
def check_cookie(request):
    d = request.COOKIES.keys()
    if "qwer" in d and "asdf" in d:
        email = request.COOKIES['qwer']
        password = request.COOKIES['asdf']
        select_user = UserInfo.objects.filter(email=email).filter(password=password)
        if len(select_user) == 0:
            return (False, -1)
        else:
            return (True, select_user[0])
    else:
        return (False, -1)

# 然后，代码定义了一个名为 `is_login` 的装饰器函数。该函数使用 `wraps` 装饰器将被装饰的函数的元数据复制到内部函数中。内部函数首先调用
# `check_cookie` 函数来检查用户是否已登录。如果已登录，内部函数将调用被装饰的函数并返回其结果。否则，内部函数将渲染一个登录页面并返回。
def is_login(func):
    @wraps(func)
    def inner(request, *args, **kwargs):
        (flag, rank) = check_cookie(request)
        if flag:
            return func(request, *args, **kwargs)
        else:
            return render(request, 'account/page-login.html', {'error_msg': ''})
    return inner

# 接下来，代码定义了一个名为 `check_login` 的函数。该函数通过查询 `UserInfo` 模型来检查给定的电子邮件和密码是否有效。如果查询结果为空，
# 函数返回False，否则返回True。
def check_login(email, password):
    select_user = UserInfo.objects.filter(email=email).filter(password=password)

    if len(select_user) == 0:
        return False
    # elif len(select_username) == 0:
    #     return False
    else:
        return True


# 然后，代码定义了两个函数 `get_all_class` 和 `get_all_type` ，它们分别返回所有的 `ClassInfo` 和 `UserType` 对象。
def get_all_class():
    return  ClassInfo.objects.all()

def get_all_type():
    return  UserType.objects.all()

# 最后，代码定义了一个名为 `DecimalEncoder` 的自定义JSON编码器类。该类重写了 `default` 方法，用于将 `decimal.Decimal` 对象转换为浮点数。
# 如果对象不是 `decimal.Decimal` 类型，则调用父类的 `default` 方法处理。
# 总之，这段代码主要用于检查用户是否已登录，并提供了一些其他的辅助函数和类来处理用户信息和数据编码。
class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj,decimal.Decimal):
            return float(obj)
        return super(DecimalEncoder,self).default(obj)