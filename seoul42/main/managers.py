from django.db import models


class CoalitionManager(models.Manager):
	def create(self, id: int = None, name: str = None, color: str = None):
		# Coalition 모델을 생성하는 메소드
		coalition = self.model(
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
			coalition = None,
			coalition_point: int = None,
	):
		# FtUser 모델을 생성하는 메소드
		ft_user = self.model(
			id=id,
			login=login,
			is_alive=is_alive,
			coalition=coalition,
			coalition_point=coalition_point,
		)
		ft_user.save(using=self._db)
		return ft_user
