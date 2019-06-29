from django.db import models

# Create your models here.
class Vip(models.Model):
    """VIP会员模型"""
    name = models.CharField(max_length=64, verbose_name='会员名称')

    level = models.IntegerField(default=0, verbose_name='等级')

    price = models.FloatField(verbose_name='价格')

    def __str__(self):
        return f'<{self.name}>'

    # 检查当前vip是否具有某个权限
    def has_perm(self, perm):
        # 先根据vip的id从vip和权限的关系表中把数据查出来.
        relation = VipPermRelation.objects.filter(vip_id=self.id).only('perm_id')
        perm_id_list = [r.perm_id for r in relation]
        if perm.id in perm_id_list:
            return True
        return False


class Permission(models.Model):
    """权限模型"""
    name = models.CharField(max_length=64, verbose_name='权限名称')

    description = models.TextField(verbose_name='权限说明')


# 定义vip和权限的中间表
class VipPermRelation(models.Model):
    vip_id = models.IntegerField()
    perm_id = models.IntegerField()