from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from datetime import datetime, timedelta
from decimal import Decimal

from main.custom import count_page, SuperUserCheckMixin
from main.ftapi import FtApi
from .models import FtUser, Coalition, FtPool, FtUserProject, FtCursus, FtProject, Tier


class MakePiscineFtUser(SuperUserCheckMixin, View):
	"""
	42 한국 캠퍼스 유저들중 피신중인 유저를 생성함
	"""

	@staticmethod
	def is_piscine_user(end):
		end_date = datetime.strptime(end.split('.')[0], '%Y-%m-%dT%H:%M:%S')
		now_date = datetime.now()
		return 1 if (end_date - now_date).days >= 0 else 0

	def post(self, request):
		ft_api: FtApi = FtApi()
		page: int = count_page(ft_api.get_data(url="campus/29")["users_count"])
		crawlings = [ft_api.get_data(url="campus/29/users", page=x, per_page=100, sort="login")
		             for x in range(1, int(page) + 1)]
		for crawling in crawlings:
			for user_data in crawling:
				if not FtUser.objects.filter(login=user_data["login"]).exists():
					user_detail_data = ft_api.get_data(url=f'users/{user_data["login"]}')

		return render(request, "piscine/piscine_manage_complete.html", {"task": "MakePiscineFtUser"})
