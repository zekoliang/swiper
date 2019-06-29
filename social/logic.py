import logging
import datetime

from django.core.cache import cache

from common import keys
from lib.cache import rds
from social.models import Swipe, Friend
from swiper import config
from user.models import User
from common import errors

logger = logging.getLogger('err')

def like(uid, sid):
    Swipe.like(uid, sid)

    # 检查对方是否喜欢自己.
    if Swipe.has_like_me(sid, uid):
        # 喜欢的话就建立好友关系
        uid1, uid2 = (uid, sid) if uid < sid else (sid, uid)
        Friend.make_friends(uid1=uid1, uid2=uid2)
        return True
    return False


def superlike(uid, sid):
    Swipe.superlike(uid, sid)
    if Swipe.has_like_me(sid, uid):
        uid1, uid2 = (uid, sid) if uid < sid else (sid, uid)
        Friend.make_friends(uid1=uid1, uid2=uid2)
        return True
    return False


def get_rcmd_list(user):
    """
    :return: [user1, user2, user2]
    """
    # 已经滑过的人不能再滑
    swiped_list = Swipe.objects.filter(uid=user.id).only('sid')
    sid_list = [s.sid for s in swiped_list]
    # 推荐用户中不能出现自己
    sid_list.append(user.id)

    current_year = datetime.datetime.now().year
    mix_birth_day = current_year - user.profile.max_dating_age
    max_birth_day = current_year - user.profile.min_dating_age
    users = User.objects.filter(location=user.profile.location,
                        birth_year__range=(mix_birth_day, max_birth_day),
                        sex=user.profile.dating_sex).exclude(id__in=sid_list)[:20]
    return users


def rewind(user):
    now = datetime.datetime.now()
    key = keys.REWIND_KEY % now.date()
    rewind_times = cache.get(key, 0)  # 取不到给一个默认值0
    if rewind_times < config.REWIND_TIMES:
        # 可以执行反悔操作
        # 删除最近的滑动记录
        record = Swipe.objects.filter(uid=user.id).latest(field_name='time')
        # 判断是否有好友关系
        uid1, uid2 = (user.id, record.sid) if user.id < record.sid else (record.sid, user.id)
        friends = Friend.objects.filter(uid1=uid1, uid2=uid2)
        friends.delete()

        # 更新缓存中的反悔次数
        rewind_times += 1
        timeout = 86400 - (now.hour * 60 * 60 + now.minute * 60 + now.second)
        cache.set(key, rewind_times, timeout)

        key = keys.HOT_RANK_KEY % record.sid
        # 处理反悔之后的排名得分问题
        # if record.mark == 'like':
        #     # 减5分
        #     rds.zincrby(config.RANK_KEY, -config.LIKE_SCORE, key)
        # elif record.mark == 'dislike':
        #     rds.zincrby(config.RANK_KEY, -config.DISLIKE_SCORE, key)
        # else:
        #     rds.zincrby(config.RANK_KEY, -config.SUPERLIKE_SCORE, key)
        # 优化
        mapping = {
            'like': config.LIKE_SCORE,
            'dislike': config.DISLIKE_SCORE,
            'superlike': config.SUPERLIKE_SCORE
        }
        rds.zincrby(config.RANK_KEY, -mapping[record.mark], key)

        record.delete()
    else:
        logger.error('exceed the maxmium rewind times')
        raise errors.RewindErr


def get_top_n():
    """
        {
            code:0,
            data: [
                {rank:1,
                 score;100,
                 nickname: nickname,
                 ...},
                {}
            ]
        }
        """
    # [[b'11', 7.0], [b'2', 5.0], [b'3', -5.0]]
    rank_list = rds.zrevrange(config.RANK_KEY, 0, -1, withscores=True)
    # 清洗一下数据, 转成int型
    clean_data = [(int(id), int(score)) for (id, score) in rank_list]
    # clean_data中取出id
    id_list = [item[0] for item in clean_data]

    # users = []
    # for id in id_list:
    #     user = User.get(id=id)
    #     users.append(user)
    # 推荐以下写法
    # django默认会根据对象id进行排序,是从小到大的.
    users = User.objects.filter(id__in=id_list)
    # 对users排序
    users = sorted(users, key=lambda user: id_list.index(user.id))

    top_n = []
    for rank, (_, score), user in zip(range(1, config.TOP_N + 1), clean_data, users):
        data = dict()
        data['rank'] = rank
        data['score'] = score
        data.update(user.to_dict())
        top_n.append(data)

    return top_n