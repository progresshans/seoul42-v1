from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin


class CanSeePiscineCheckMixin(UserPassesTestMixin, View):
	"""슈퍼 유저인지 확인하는 Mixin"""

	def test_func(self):
		return self.request.user.can_see_piscine
