

import hashlib

str = "123456"
a = hashlib.sha1(str.encode("utf-8")).hexdigest()
print("sha1加密前为 ：", str)
print("sha1加密前后 ：", a)

"""
sha1加密前为 ： 中国你好
sha1加密前后 ： 3e6c570876775d0031dbf66247ed1054d4ef695e
"""
