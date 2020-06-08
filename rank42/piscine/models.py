from datetime import datetime

from django.db import models
from .managers import PiscineFtUserManager


class PiscineProject(models.Model):
	id: int = models.IntegerField(unique=True, primary_key=True)
	name: str = models.CharField(verbose_name="과제 이름", max_length=50)


class TempFtUser(models.Model):
	id: int = models.IntegerField(unique=True, primary_key=True)


class PiscineFtUser(models.Model):
	id: int = models.IntegerField(unique=True, primary_key=True)
	login: str = models.CharField(verbose_name="로그인 아이디", max_length=20)
	is_public: bool = models.BooleanField(verbose_name="공개여부", default=False)
	piscine_level = models.DecimalField(verbose_name="피씬레벨", max_digits=4, decimal_places=2)
	piscine_projects = models.ManyToManyField(PiscineProject, blank=True)
	created_at: datetime = models.DateTimeField(auto_now_add=True)
	updated_at: datetime = models.DateTimeField(auto_now=True)

	objects = PiscineFtUserManager()