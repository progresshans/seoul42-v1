from datetime import datetime

from django.db import models
from .managers import FtUserManager, CoalitionManager


# Create your models here.
class Coalition(models.Model):
	id: int = models.IntegerField(unique=True, primary_key=True)
	name: str = models.CharField(verbose_name="길드 이름", max_length=50)
	color: str = models.CharField(verbose_name="길드 색상", max_length=7)
	created_at: datetime = models.DateTimeField(auto_now_add=True)
	updated_at: datetime = models.DateTimeField(auto_now=True)

	objects = CoalitionManager()


class FtUser(models.Model):
	id: int = models.IntegerField(unique=True, primary_key=True)
	login: str = models.CharField(verbose_name="로그인 아이디", max_length=20)
	is_alive: bool = models.BooleanField(verbose_name="생존여부", default=False)
	coalition: Coalition = models.ForeignKey(Coalition, verbose_name="길드", on_delete=models.CASCADE, blank=True, null=True)
	coalition_point: int = models.IntegerField(verbose_name="길드 포인트", blank=True, null=True)
	created_at: datetime = models.DateTimeField(auto_now_add=True)
	updated_at: datetime = models.DateTimeField(auto_now=True)

	objects = FtUserManager()


class Tier(models.Model):
	FtUser: FtUser = models.OneToOneField(FtUser, on_delete=models.CASCADE, primary_key=True)
	coalition_point: int = models.IntegerField(verbose_name="길드 포인트", blank=True, null=True)
	tier_name: str = models.CharField(max_length=13, blank=True, null=True)
	tier_rank: str = models.IntegerField(blank=True, null=True)
	created_at: datetime = models.DateTimeField(auto_now_add=True)
	updated_at: datetime = models.DateTimeField(auto_now=True)


class UpdateBranch(models.Model):
	id: int = models.AutoField(primary_key=True)
	is_updating: bool = models.BooleanField()
	created_at: datetime = models.DateTimeField(auto_now_add=True)
	updated_at: datetime = models.DateTimeField(auto_now=True)


class PointLog(models.Model):
	id: int = models.AutoField(primary_key=True)
	ft_user: FtUser = models.ForeignKey(FtUser, on_delete=models.CASCADE)
	update_branch: UpdateBranch = models.ForeignKey(UpdateBranch, on_delete=models.CASCADE)
	coalition_point: int = models.IntegerField(verbose_name="길드 포인트")
	created_at: datetime = models.DateTimeField(auto_now_add=True)
	updated_at: datetime = models.DateTimeField(auto_now=True)