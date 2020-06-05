"""
기능이 필요해서 만든 custom 함수나 class 들
"""
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin


def count_page(number: int) -> int:
	"""총 유저 수를 가지고 100으로 나눠 api가 파싱해야하는 총 페이지 수를 반환"""
	if int(number) <= 100:
		return 1
	page: float = int(number) / 100
	page: int = int(page) + 1 if number % (100 * int(page)) != 0 else int(page)
	return page


class SuperUserCheckMixin(UserPassesTestMixin, View):
	"""슈퍼 유저인지 확인하는 Mixin"""

	def test_func(self):
		return self.request.user.is_superuser
