from django.contrib.auth.backends import ModelBackend
from .models import MyUser


class RequestAuthBackend(ModelBackend):
    def authenticate(self, request, login=None, **kwargs):
        try:
            user = MyUser.objects.get(login=login)
            if request.session['login_user'] == user:
                return user
            else:
                return None
        except MyUser.DoesNotExist:
            return None
