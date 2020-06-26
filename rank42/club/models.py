from django.db import models
from django.conf import settings


class Club(models.Model):
    id = models.AutoField(primary_key=True)
    master = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.PROTECT)
    name = models.CharField(verbose_name="소모임 이름", max_length=100)
    content = models.TextField(verbose_name="소모임 소개")
    can_join = models.BooleanField(verbose_name="가입가능여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_absolute_url(self):
        return f'/club/{self.id}/'


class ClubMember(models.Model):
    id = models.AutoField(primary_key=True)
    club = models.ForeignKey(Club, related_name='members', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    introducing = models.TextField(verbose_name="자기소개")
    is_join = models.BooleanField(verbose_name="가입여부")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)