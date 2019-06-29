import datetime

from django.db import models

from lib.orm import ModelMixin

from social.models import Swipe
from vip.models import Vip

SEX = (
        ('female', 'female'),
        ('male', 'male'),
    )

class User(models.Model):
    """
    用户模型
    """
    phonenum = models.CharField(max_length=20, unique=True, verbose_name='手机号')

    nickname = models.CharField(max_length=128, unique=True, verbose_name='昵称')

    sex = models.CharField(max_length=20, choices=SEX, verbose_name='性别')

    birth_year = models.IntegerField(default=2000, verbose_name='出生年')

    birth_month = models.IntegerField(default=1, verbose_name='出生月')

    birth_day = models.IntegerField(default=1, verbose_name='出生日')

    avatar = models.CharField(max_length=256, verbose_name='个人形象')

    location = models.CharField(max_length=64, verbose_name='常居地')

    # 用户的vip等级
    vip_id = models.IntegerField(default=1, verbose_name='用户vip等级')

    @property
    def vip(self):
        return Vip.get(id=self.vip_id)

    def __str__(self):
        return f'<User {self.nickname}>'


    class Meta:
        db_table = 'user'

    @property
    def age(self):
        today = datetime.datetime.today()
        birthday = datetime.datetime(year=self.birth_year,
                                     month=self.birth_month,
                                     day=self.birth_day)
        return (today - birthday).days // 365

    def to_dict(self):
        """把对象的信息用字典形式表示"""
        return {
            'phonenum' : self.phonenum,
            'nickname' : self.nickname,
            'sex' : self.sex,
            'age': self.age,
            'avatar' : self.avatar,
            'location' : self.location,
        }

    @property
    def profile(self):
        # 获取用户的profile
        # print(hasattr(self, 'profile_'))
        if not hasattr(self, 'profile_'):
            self.profile_, _ = Profile.get_or_create(id=self.id)
            print('get from database')
        # print('get from self')
        return self.profile_


    # 查看喜欢我的人
    def like_me(self):
        swipers = Swipe.objects.filter(sid=self.id, mark__in=['like', 'superlike']).only('uid')
        uid_list = [u.uid for u in swipers]
        users = User.objects.filter(id__in=uid_list)
        return users


class Profile(models.Model):
    """
    用户个人资料模型
    """
    location = models.CharField(max_length=64, verbose_name='目标城市')

    min_distance = models.IntegerField(default=0, verbose_name='最小查找范围')

    max_distance = models.IntegerField(default=50, verbose_name='最大查找范围')

    min_dating_age = models.IntegerField(default=18, verbose_name='最小交友年龄')

    max_dating_age = models.IntegerField(default=50, verbose_name='最大交友年龄')

    dating_sex = models.CharField(max_length=20, choices=SEX, verbose_name='匹配的性别')

    vibration = models.BooleanField(default=True, verbose_name='开启震动')

    only_matche = models.BooleanField(default=True, verbose_name='不让为匹配的人看我的相册')

    auto_play = models.BooleanField(default=True, verbose_name='自动播放视频')

    class Meta:
        db_table = 'profile'

    # def to_dict(self):
    #     return {
    #         'location' : self.location,
    #         'min_distance' : self.min_distance,
    #         'max_distance' : self.max_distance,
    #         'min_dating_age' : self.min_dating_age,
    #         'max_dating_age' : self.max_dating_age,
    #         'dating_sex' : self.dating_sex,
    #         'vibration' : self.vibration,
    #         'only_matche' : self.only_matche,
    #         'auto_play' : self.auto_play,
    #     }
