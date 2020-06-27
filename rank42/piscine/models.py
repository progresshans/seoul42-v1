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
	is_pass = models.BooleanField(verbose_name="합격여부", default=False)
	created_at: datetime = models.DateTimeField(auto_now_add=True)
	updated_at: datetime = models.DateTimeField(auto_now=True)

	objects = PiscineFtUserManager()


"""
아래 코드는 개발중인 테스트 코드입니다.
Rank42 개발 초기와 따르게 점점 지원하는 기능이 늘어나면서, 모델을 땜빵식으로 확장하고 있는데,
전체적으로 깔끔하게 정리하고 통합적으로 모든 기능을 지원할 수 있는 모델 개발이 목표.

기존 모델과 겹치는 부분은 뒤에 2로 붙이고 추후 코드 통합하면서 하나로 합칠 예정.
"""


class FtCursus(models.Model):


class FtProject(models.Model):
	PROJECT_TYPE = (
		('assignment', '과제'),
		('rush', '러쉬'),
		('exam', '시험'),
	)
	id = models.IntegerField()
	type = models.CharField(max_length=10, choices=PROJECT_TYPE)
	name = models.CharField(max_length=50)
	slug = models.CharField(max_length=50)


class FtUserProject(models.Model):
	id = models.IntegerField()


class FtPool(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=20)
	month = models.CharField(max_length=15)
	year = models.CharField(max_length=10)


class FtUser2(models.Model):
	id = models.IntegerField()
	email = models.EmailField(verbose_name="이메일")
	login = models.CharField(verbose_name="로그인 아이디", max_length=30, primary_key=True)
	image_url = models.URLField(verbose_name="프로필사진")
	is_ft_staff = models.BooleanField(verbose_name="스태프여부")
	ft_pool = models.ForeignKey()
	piscine_level = models.DecimalField(verbose_name="피신 레벨", max_digits=4, decimal_places=2)
	main_level = models.DecimalField(verbose_name="본과 레벨", max_digits=4, decimal_places=2, blank=True, null=True)


