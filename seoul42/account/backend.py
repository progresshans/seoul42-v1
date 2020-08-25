from django.contrib.auth.backends import ModelBackend
from .models import MyUser


class RequestAuthBackend(ModelBackend):
    def authenticate(self, request, login=None, **kwargs):
        try:
            user = MyUser.objects.get(login=login)
            return user
        except MyUser.DoesNotExist:
            return None

    def get_user(self, login):
        try:
            return MyUser.objects.get(login=login)
        except MyUser.DoesNotExist:
            return None
