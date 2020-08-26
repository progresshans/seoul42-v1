"""
개발환경에서 사용되는 설정
"""
from .base import *

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True


ALLOWED_HOSTS = [
    'localhost',
    '127.0.0.1',
]

# secret_info_file.json 파일 위치를 명시
SECRET_INFO_FILE = os.path.join(BASE_DIR, 'config', 'settings', 'secret_info_file.json')

with open(SECRET_INFO_FILE) as f:
    secrets = json.loads(f.read())

def get_secret(setting, secrets=secrets):
    """비밀 변수를 가져오거나 명시적 예외를 반환한다."""
    try:
        return secrets[setting]
    except KeyError:
        error_msg = f"Set the {setting} environment variable"
        raise ImproperlyConfigured(error_msg)


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/3.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = os.environ.get('DJANGO_SECRET_KEY', '9=m!n=s%nos73$$h&!ty45$e-$a)m-as4i)^bf8#_ve4ocw#3+')
FT_UID_KEY = os.environ.get('FT_UID_KEY', get_secret("FT_UID_KEY"))
FT_SECRET_KEY = os.environ.get('FT_SECRET_KEY', get_secret("FT_SECRET_KEY"))


# Database
# https://docs.djangoproject.com/en/3.0/ref/settings/#databases

DATABASES = {
    # sqlite3는 비동기 처리시 동시에 발생하는 커넥션을 감당못함
    # 'default': {
    #     'ENGINE': 'django.db.backends.sqlite3',
    #     'NAME': os.path.join(BASE_DIR, 'db.sqlite3'),
    # }

    'default': {
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': 'seoul42',
        'USER': 'seoul42',
        'PASSWORD': 'seoul42',
        'HOST': 'db',
        'PORT': '5432'
    }
}

AM_I_HTTPS = "http"
