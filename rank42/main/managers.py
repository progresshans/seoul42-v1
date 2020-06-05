from typing import Sequence, Union
from django.db import models

from .models import Coalition, FtUser


class CoalitionManager(models.Manager):
	def create(self, id: int = None, name: str = None, color: str = None) -> Coalition:
		coalition: Coalition = self.model(
			id=id,
			name=name,
			color=color,
		)
		coalition.save(using=self._db)
		return coalition


class FtUserManager(models.Manager):
	def create(
			self,
			id: int = None,
			login: str = None,
			is_alive: bool = None,
			coalition: Coalition = None,
			coalition_point: int = None,
	) -> FtUser:
		ft_user: FtUser = self.model(
			id=id,
			login=login,
			is_alive=is_alive,
			coalition=coalition,
			coalition_point=coalition_point,
		)
		ft_user.save(using=self._db)
		return ft_user
