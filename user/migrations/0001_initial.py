# -*- coding: utf-8 -*-
# Generated by Django 1.11.18 on 2019-06-27 13:34
from __future__ import unicode_literals

from django.db import migrations, models
import lib.orm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('location', models.CharField(max_length=64, verbose_name='目标城市')),
                ('min_distance', models.IntegerField(default=0, verbose_name='最小查找范围')),
                ('max_distance', models.IntegerField(default=50, verbose_name='最大查找范围')),
                ('min_dating_age', models.IntegerField(default=18, verbose_name='最小交友年龄')),
                ('max_dating_age', models.IntegerField(default=50, verbose_name='最大交友年龄')),
                ('dating_sex', models.CharField(choices=[('female', 'female'), ('male', 'male')], max_length=20, verbose_name='匹配的性别')),
                ('vibration', models.BooleanField(default=True, verbose_name='开启震动')),
                ('only_matche', models.BooleanField(default=True, verbose_name='不让为匹配的人看我的相册')),
                ('auto_play', models.BooleanField(default=True, verbose_name='自动播放视频')),
            ],
            options={
                'db_table': 'profile',
            },
            bases=(models.Model, lib.orm.ModelMixin),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('phonenum', models.CharField(max_length=20, unique=True, verbose_name='手机号')),
                ('nickname', models.CharField(max_length=128, unique=True, verbose_name='昵称')),
                ('sex', models.CharField(choices=[('female', 'female'), ('male', 'male')], max_length=20, verbose_name='性别')),
                ('birth_year', models.IntegerField(default=2000, verbose_name='出生年')),
                ('birth_month', models.IntegerField(default=1, verbose_name='出生月')),
                ('birth_day', models.IntegerField(default=1, verbose_name='出生日')),
                ('avatar', models.CharField(max_length=256, verbose_name='个人形象')),
                ('location', models.CharField(max_length=64, verbose_name='常居地')),
                ('vip_id', models.IntegerField(default=1, verbose_name='用户vip等级')),
            ],
            options={
                'db_table': 'user',
            },
        ),
    ]
