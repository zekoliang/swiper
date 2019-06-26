from django.utils.deprecation import MiddlewareMixin

from common import errors
from lib.http import render_json
from user.models import User


class AuthMiddleware(MiddlewareMixin):
    def process_request(self, request):
        # 白名单
        WHITE_LIST = [
            '/api/user/submit/phone/',
            '/api/user/submit/vcode/'
        ]

        if request.path in WHITE_LIST:
            return
        uid = request.session.get('uid')
        if uid:
            try:
                user = User.objects.get(id=uid)
                request.user = user
                return
            except User.DoesNotExist:
                return render_json(code=errors.USER_NOT_EXIST, data='用户不存在')
        else:
            return render_json(code=errors.LOGIN_REQUIRED, data='请登录')