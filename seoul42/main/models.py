from datetime import datetime

from django.db import models
from .managers import FtUserManager, CoalitionManager


# Create your models here.
class Coalition(models.Model):
	id = models.IntegerField(unique=True, primary_key=True)
	name = models.CharField(verbose_name="길드 이름", max_length=50)
	color = models.CharField(verbose_name="길드 색상", max_length=7)
	created_at: datetime = models.DateTimeField(auto_now_add=True)
	updated_at: datetime = models.DateTimeField(auto_now=True)

	objects = CoalitionManager()


class FtUser(models.Model):
	id = models.IntegerField(unique=True, primary_key=True)
	login = models.CharField(verbose_name="로그인 아이디", max_length=20)
	data = models.JSONField(blank=True, null=True)
	is_alive = models.BooleanField(verbose_name="생존여부", default=False)
	coalition = models.ForeignKey(
		Coalition,
		verbose_name="길드",
		on_delete=models.CASCADE,
		blank=True,
		null=True,
	)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	# objects = FtUserManager()


class Tier(models.Model):
	FtUser = models.OneToOneField(FtUser, on_delete=models.CASCADE, primary_key=True)
	coalition_point = models.IntegerField(verbose_name="길드 포인트", blank=True, null=True)
	tier_name = models.CharField(max_length=13, blank=True, null=True)
	tier_rank = models.IntegerField(blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class TierLog(models.Model):
	id = models.AutoField(primary_key=True)
	ft_user = models.ForeignKey(FtUser, on_delete=models.CASCADE)
	coalition_point = models.IntegerField(verbose_name="길드 포인트")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class ApiKey(models.Model):
	id = models.AutoField(primary_key=True)
	name = models.CharField(max_length=20, blank=True, null=True)
	uid = models.CharField(max_length=100)
	secret = models.CharField(max_length=100)
