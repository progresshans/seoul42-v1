import os

broker_url = os.environ.get('REDIS_URL', 'redis://localhost:6379')
result_backend = 'django-db'

task_serializer = 'json'
result_serializer = 'json'
accept_content = ['json']
timezone = 'Asia/Seoul'
enable_utc = True
