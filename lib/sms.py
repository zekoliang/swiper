import random

import requests
from django.core.cache import cache

from swiper import config
from common import keys
from worker import celery_app



def gen_vcode(size=4):
    """0000-9999"""
    start = 10 **(size - 1)
    end = 10 ** size - 1
    return random.randint(start, end)


@celery_app.task
def send_vcode(phone):
    params = config.YZX_PARAMS.copy()
    params['mobile'] = phone
    vcode = gen_vcode()
    params['param'] = vcode
    # 存入缓存 超时时间180秒
    cache.set(keys.VCODE_KEY % phone, str(vcode), timeout=180)
    resp = requests.post(config.YZX_URL, json=params)
    if resp.status_code == 200:
        # ok
        result = resp.json()
        if result['code'] == '000000':
            return 'OK'
        else:
            return result['msg']
    else:
        return '发送短信有误'