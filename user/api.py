import os
from urllib.parse import urljoin

from django.core.cache import cache
from django.conf import settings

from lib.sms import  send_vcode
from common import errors
from lib.http import render_json
from common import keys
from user.models import User
from .forms import ProfileForm
from .logic import handle_uploaded_file
from lib.qiniu import upload_qiniu
from swiper import config
# Create your views here.


def submit_phone(request):
    """提交手机号码"""
    phone = request.POST.get('phone')
    # 给这个手机号码发短信.
    msg = send_vcode(phone)
    if msg == 'OK':
        return render_json()
    return render_json(code=errors.SMS_ERROR, data=msg)


def submit_vcode(request):
    """通过验证码登录、注册"""
    phone = request.POST.get('phone')
    vcode = request.POST.get('vcode')

    # 从缓存中取
    cached_vcode = cache.get(keys.VCODE_KEY % phone)
    if vcode == cached_vcode:
        # 登录或者注册成功
        # 如果是注册的话, 在数据库中创建用户.
        # 如果是登录的话,直接从数据查询用户,返回用户信息.
        # try:
        #     user = User.objects.get(phonenum=phone)
        # except User.DoesNotExist:
        #     # 说明是注册
        #     # 去数据库中创建用户
        #     user = User.objects.create(phonenum=phone, nick=phone)

        user, created = User.objects.get_or_create(phonenum=phone,
                                        defaults={'nickname': phone})
        print(created)
        request.session['uid'] = user.id
        return render_json(data=user.to_dict())
    return render_json(code=errors.VCODE_ERROR, data='验证码错误')


def get_profile(request):
    """获取个人资料"""
    # uid = request.session.get('uid')
    # user = User.objects.get(id=uid)
    user = request.user
    return render_json(data=user.profile.to_dict())


def edit_profile(request):
    """修改个人资料"""
    user = request.user
    form = ProfileForm(request.POST)
    if form.is_valid():
        profile = form.save(commit=False)
        profile.id = user.id
        profile.save()
        return render_json(data=profile.to_dict())
    return render_json(code=errors.PROFILE_ERR, data=form.errors)


def upload_avatar(request):
    """头像上传"""
    avater = request.FILES.get('avater')
    user = request.user

    uid = request.user.id
    # 保存到本地
    handle_uploaded_file(uid, avater)

    # 上传到七牛云
    flag = upload_qiniu(uid)
    if flag:
        # 拼接地址
        avater_url = urljoin(config.QIUNIU_URL, keys.AVATAR_KEY % uid)
        user.avatar = avater_url
        user.save()
        return render_json(data='上传成功')
    return render_json(code=errors.AVATAR_ERR, data='上传七牛云失败')

