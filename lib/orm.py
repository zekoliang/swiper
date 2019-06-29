from django.core.cache import cache
from django.db import models

from common import keys


class ModelMixin:
    def to_dict(self):
        att_dict = {}
        for field in self._meta.get_fields():
            att_dict[field.attname] = getattr(self, field.attname, None)
        return att_dict

        # 对get返回的对象做缓存
        # def get(cls, *args, **kwargs):
        #     obj = cache.get(key)
        #     if not obj:
        #         obj = cls.get(*args, **kwargs)



def get(cls, *args, **kwargs):
    # 先从缓存中取数据
    # 只针对主键和id的查询进行缓存
    pk = kwargs.get('id') or kwargs.get('pk')
    if pk:
        # 如果是主键的话才去做缓存
        key = keys.OBJ_KEY % pk
        obj = cache.get(key)
        if not obj:
            # 从数据库中拿
            obj = cls.objects.get(pk=pk)
            print('get object from database')
            # 存入缓存
            cache.set(key, obj, 86400 * 15)
    else:
        obj = cls.objects.get(*args, **kwargs)
    return obj


def get_or_create(cls, *args, **kwargs):
    pk = kwargs.get('id') or kwargs.get('pk')
    if pk:
        # 如果是主键的话才去做缓存
        key = keys.OBJ_KEY % pk
        obj = cache.get(key)
        if not obj:
            # 从数据库中拿

            obj = cls.objects.get_or_create(pk=pk)
            print('get object from database')
            # 存入缓存
            cache.set(key, obj, 86400 * 15)
    else:
        obj = cls.objects.get_or_create(*args, **kwargs)
    return obj


def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
    # 先执行原来的save方法,存入数据库
    self.ori_save()
    # 更新缓存
    key = keys.OBJ_KEY % self.id
    cache.set(key, self, 86400 * 15)


def to_dict(self):
    att_dict = {}
    for field in self._meta.get_fields():
        att_dict[field.attname] = getattr(self, field.attname, None)
    return att_dict


def model_patch():  # 猴子补丁
    models.Model.get = classmethod(get)  # = @classmethod
    models.Model.get_or_create = classmethod(get_or_create)
    # 把原生的save取个别名
    models.Model.ori_save = models.Model.save
    models.Model.save = save

    models.Model.to_dict = to_dict