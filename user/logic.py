import os

from django.conf import settings

from common import keys
from lib.qiniu import upload_qiniu
from worker import celery_app


@celery_app.task
def handle_uploaded_file(uid, avater):
    """头像文件上传"""
    filename = keys.AVATAR_KEY % uid
    filepath = os.path.join(settings.BASE_DIR, settings.MEDIA_ROOT, filename)
    with open(filepath, mode='wb+') as fp:
        for chunk in avater.chunks():
            fp.write(chunk)

    # 上传到七牛云
    upload_qiniu(uid)
