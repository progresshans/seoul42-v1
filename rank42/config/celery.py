from __future__ import absolute_import, unicode_literals

import os
from celery import Celery

# '셀러리' 프로그램을 위해 기본 장고 설정파일을 설정합니다.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings.development')

app = Celery('tasks')

app.config_from_object('config.settings.celery_config')

# 등록된 장고 앱 설정에서 task를 불러옵니다.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
	print('Request: {0!r}'.format(self.request))
