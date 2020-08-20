"""
프로덕션 환경에서 사용되는 설정값
현재 heroku 환경에서 작동중
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY')
FT_UID_KEY = os.environ.get('FT_UID_KEY')
FT_SECRET_KEY = os.environ.get('FT_SECRET_KEY')


ALLOWED_HOSTS = [
    '.seoul42.com',
    '.herokuapp.com',
]


DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    }
}

# Heroku: Update database configuration from $DATABASE_URL.
import dj_database_url
db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

AM_I_HTTPS = "https"
