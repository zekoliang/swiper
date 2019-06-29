import datetime

from django.core.cache import cache

from lib.cache import rds
from lib.http import render_json
from social.models import Swipe, Friend
from swiper import config
from user.models import User
from vip.logic import need_perm
from . import logic
from common import keys, errors


def get_recommend_list(request):
    """获取推荐列表"""
    user = request.user
    users =logic.get_rcmd_list(user)
    data = [user.to_dict() for user in users]
    return render_json(data=data)


def like(request):
    """喜欢"""
    user = request.user
    # 在swipe中创建一条记录.
    sid = request.POST.get('sid')
    flag = logic.like(user.id, int(sid))

    # 喜欢加5分
    key = keys.HOT_RANK_KEY % sid
    rds.zincrby(config.RANK_KEY, config.LIKE_SCORE, key)

    if flag:
        return render_json(data={'matched': True})
    return render_json(data={'matched': False})


def dislike(request):
    """不喜欢"""
    user = request.user
    sid = request.POST.get('sid')
    Swipe.dislike(uid=user.id, sid=int(sid))

    # 不喜欢减5分
    key = keys.HOT_RANK_KEY % sid
    rds.zincrby(config.RANK_KEY, config.DISLIKE_SCORE, key)
    return render_json()


@need_perm('superlike')
def superlike(request):
    """超级喜欢"""
    user = request.user
    # 在swipe中创建一条记录.
    sid = request.POST.get('sid')
    flag = logic.superlike(user.id, int(sid))

    # 超级喜欢加7分
    key = keys.HOT_RANK_KEY % sid
    rds.zincrby(config.RANK_KEY, config.SUPERLIKE_SCORE, key)

    if flag:
        return render_json(data={'matched': True})
    return render_json(data={'matched': False})


@need_perm('rewind')
def rewind(request):
    """反悔 (每天允许返回 3 次) 只允许反悔上一次操作"""
    # 删除最近滑动记录.
    # 如果有好友关系的话,好友关系也要撤销.
    # 每次执行反悔操作之前,先从缓存中取出来已经操作次数.进行对比,如果小于3就可以继续操作.
    # 从缓存中取
    user = request.user
    logic.rewind(user)
    return render_json()


@need_perm('liked_me')
def liked_me(request):
    """查看喜欢过我的人"""
    user = request.user
    users = user.like_me()
    data = [u.to_dict() for u in users]
    return render_json(data=data)


def get_top_n(request):
    """排行榜"""
    data = logic.get_top_n()
    return render_json(data=data)