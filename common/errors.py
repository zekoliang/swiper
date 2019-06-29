"""定制 错误码"""
SMS_ERROR = 1000    # 短信发送错误
VCODE_ERROR = 1001  # 短信验证码错误
LOGIN_REQUIRED = 1002   # 用户名未登录错误
USER_NOT_EXIST = 1003   # 用户不存在错误
PROFILE_ERR = 1004  # 数据不合法错误
AVATAR_ERR = 1005   # 头像上传七牛云失败错误
REWIND_ERR = 1006   # 超过最大反悔次数


# Error改写成类

# 基类
class LogicErr(Exception):
    code = None
    data = None

    def __str__(self):
        return f'<{self.__class__.__name__}>'


def gen_error_class(name, code, data):
    return type(name, (LogicErr,), {'code': code, 'data': data})


# 生成各种类

SmsError = gen_error_class('SmsError', code=1000, data='短信发送错误')
VcodeError = gen_error_class('VcodeError', code=1001, data='验证码错误')
LoginRequired = gen_error_class('LoginRequired', code=1002, data='请登录')
UserNotExist = gen_error_class('UserNotExist', code=1003, data='用户不存在')
ProfileErr = gen_error_class('ProfileErr', code=1004, data='个人资料错误')
AvatarErr = gen_error_class('AvatarErr', code=1005, data='头像上传失败')
RewindErr = gen_error_class('RewindErr', code=1006, data='超过最大反悔次数')
PermissionRequired = gen_error_class('PermissionRequired',code=1007, data='权限不足,请充值')
