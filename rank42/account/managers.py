from django.contrib.auth.models import BaseUserManager
from .custom import get_random_string


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
		user.save(using=self._db)
		return user
