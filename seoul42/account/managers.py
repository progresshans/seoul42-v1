from django.contrib.auth.models import BaseUserManager

from .customs import get_random_string

from main.models import FtUser


class MyUserManager(BaseUserManager):
	def create_user(self, id, email, login):
		user = self.model(
			id=id,
			email=email,
			login=login,
		)
		user.set_password(get_random_string(20))
		user.save(using=self._db)
		return user

	def create_superuser(self, login, password):
		user = self.model(
			login=login
		)
		user.set_password(password)
		user.is_admin = True
		user.allow_piscine_list = True
		user.save(using=self._db)
		return user

	def set_user_type(self):
		try:
			ft_uesr = FtUser.objects.get(login=self.model.login)
			self.model.user_type = get_cursus_type(ft_user=ft_uesr)
			self.model.save()
			return True
		except:
			self.model.user_type = 0
			self.model.save()
			return False
