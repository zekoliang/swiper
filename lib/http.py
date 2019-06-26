"""封装返回json的操作"""
import json

from django.http import HttpResponse
from django.conf import settings

def render_json(code=0, data=None):
    dic = {
        'code': code,
        'data': data
    }
    if settings.DEBUG:
        dic = json.dumps(dic, indent=4, ensure_ascii=False, sort_keys=True)
    else:
        dic = json.dumps(dic, separators=[',', ':'], ensure_ascii=False)
    return HttpResponse(dic)