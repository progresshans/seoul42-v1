from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .managers import MyUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
	login = models.CharField(max_length=20, unique=True, primary_key=True)
	id = models.IntegerField(blank=True, null=True)
	email = models.EmailField(max_length=50, blank=True, null=True)
	is_active = models.BooleanField(default=True)
	allow_piscine_list = models.BooleanField(default=False)
	is_admin = models.BooleanField(default=False)

	objects = MyUserManager()

	USERNAME_FIELD = 'login'

	def __str__(self):
		return str(self.login)

	def has_perm(self, perm, obj=None):
		if perm == "admin":
			return self.is_admin
		else:
			return True

	def has_module_perms(self, app_label):
		return True

	@property
	def is_staff(self):
		return self.is_admin


class Profile(models.Model):
	user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
	github_login = models.CharField(max_length=100, blank=True, null=True)
	github_id = models.IntegerField(blank=True, null=True)
	github_bio = models.TextField(blank=True, null=True)
	github_html_url = models.URLField(blank=True, null=True)
	github_avatar_url = models.URLField(blank=True, null=True)
	github_total_star = models.IntegerField(blank=True, null=True)
