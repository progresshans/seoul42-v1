from django.db import models


class CoalitionManager(models.Manager):
	def create(self, id=None, name=None, color=None):
		coalition = self.model(
			id=id,
			name=name,
			color=color,
		)
		coalition.save(using=self._db)
		return coalition


class FtUserManager(models.Manager):
	def create(self, id=None, login=None, is_alive=None, coalition=None, coalition_point=None):
		ft_user = self.model(
			id=id,
			login=login,
			is_alive=is_alive,
			coalition=coalition,
			coalition_point=coalition_point,
		)
		ft_user.save(using=self._db)
		return ft_user
