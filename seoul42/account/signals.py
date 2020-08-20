from django.db.models.signals import post_save
from django.conf import settings

from .models import Profile, UserToken


def create_user_profile(sender, instance, created, **kwargs):
	print("asdkfnlaskndflksandlkans9390239032hek")
	if created:
		Profile.objects.create(user=instance)
		UserToken.objects.create(user=instance)


def save_user_profile(sender, instance, **kwargs):
	instance.profile.save()


post_save.connect(create_user_profile, sender=settings.AUTH_USER_MODEL)
post_save.connect(save_user_profile, sender=settings.AUTH_USER_MODEL)
