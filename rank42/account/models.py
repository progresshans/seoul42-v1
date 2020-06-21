from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import MyUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
	id = models.IntegerField(unique=True)
	email = models.EmailField(max_length=50, unique=True)
	login = models.CharField(max_length=20, unique=True)
	is_active = models.BooleanField(default=True)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'login'

	def __str__(self):
		return str(self.login)
