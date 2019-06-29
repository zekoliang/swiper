from common import errors
from vip.models import Permission


def need_perm(perm_name):
    def inner(view_func):
        def wrap(request, *args, **kwargs):
            # 找到用户的vip等级,
            user = request.user
            perm = Permission.get(name=perm_name)
            if user.vip.has_perm(perm):
                # 然后查看这个vip等级有没有这个权限.
                response = view_func(request, *args, **kwargs)
                return response
            else:
                raise errors.PermissionRequired
        return wrap
    return inner