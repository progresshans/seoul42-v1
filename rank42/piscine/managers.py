from django.db import models


class PiscineFtUserManager(models.Manager):
	def create(
			self,
			id: int = None,
			login: str = None,
			is_public=None,
			piscine_level=None,
			peer_count=None,
	):
		piscine_ft_user = self.model(
			id=id,
			login=login,
			is_public=is_public,
			piscine_level=piscine_level,
			peer_count=peer_count,
		)
		piscine_ft_user.save(using=self._db)
		return piscine_ft_user