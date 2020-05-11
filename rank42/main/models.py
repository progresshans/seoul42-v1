from django.db import models
from .manager import FtUserManager


# Create your models here.
class Coalition(models.Model):
	id = models.IntegerField(unique=True, primary_key=True)
	name = models.CharField(verbose_name="길드 이름", max_length=50)
	color = models.CharField(verbose_name="길드 색상", max_length=7)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class FtUser(models.Model):
	id = models.IntegerField(unique=True, primary_key=True)
	login = models.CharField(verbose_name="로그인 아이디", max_length=20)
	is_alive = models.BooleanField(verbose_name="생존여부")
	coalition = models.ForeignKey(Coalition, verbose_name="길드", on_delete=models.CASCADE(), blank=True, null=True)
	coalition_point = models.IntegerField(verbose_name="길드 포인트", blank=True, null=True)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = FtUserManager()


class UpdateBranch(models.Model):
	id = models.AutoField(primary_key=True)
	is_updating = models.BooleanField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class PointLog(models.Model):
	id = models.AutoField(primary_key=True)
	ft_user = models.ForeignKey(FtUser, on_delete=models.CASCADE())
	update_branch = models.ForeignKey(UpdateBranch, on_delete=models.CASCADE())
	coalition_point = models.IntegerField(verbose_name="길드 포인트")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)