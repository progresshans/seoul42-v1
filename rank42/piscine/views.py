from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from datetime import datetime, timedelta
from decimal import Decimal

from main.custom import count_page, SuperUserCheckMixin
from main.ftapi import FtApi
from .models import PiscineFtUser, PiscineProject, TempFtUser


class PiscineManagePage(SuperUserCheckMixin, TemplateView):
	template_name = "piscine/piscine_manage_page.html"


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
			for data in crawling:
				_, is_have = TempFtUser.objects.get_or_create(id=data["id"])
				if is_have:
					detail_data = ft_api.get_data(url=f'users/{data["id"]}')
					if len(detail_data["cursus_users"]) == 1 and not detail_data["cursus_users"][0]["end_at"] is None:
						if (PiscineFtUser.objects.filter(id=data["id"]).exists()
								or not self.is_piscine_user(detail_data["cursus_users"][0]["end_at"])):
							pass
						else:
							PiscineFtUser.objects.create(
								id=data["id"],
								login=data["login"],
								is_public=True,
								piscine_level=Decimal(detail_data["cursus_users"][0]["level"]),
							)
		return render(request, "piscine/piscine_manage_complete.html", {"task": "MakePiscineFtUser"})


class UpdatePiscineFtUser(SuperUserCheckMixin, View):
	"""
	피시너들의 정보를 업데이트 함.
	"""

	@staticmethod
	def is_one_hour(updated_at):
		one_hour_ago = datetime.now() - timedelta(hours=1)
		time_difference = one_hour_ago - updated_at
		return 1 if ((time_difference.seconds + (time_difference.days * 3600 * 24)) // 3600) >= 1 else 0

	def post(self, request):
		ft_api: FtApi = FtApi()
		piscine_ft_users = PiscineFtUser.objects.filter(is_public=True)
		for piscine_ft_user in piscine_ft_users:
			if self.is_one_hour(piscine_ft_user.updated_at):
				detail_data = ft_api.get_data(url=f'users/{piscine_ft_user.id}')
				piscine_ft_user.piscine_level = Decimal(detail_data["cursus_users"][0]["level"])
				if len(detail_data["cursus_users"]) == 2:
					piscine_ft_user.is_pass = True
				piscine_ft_user.save()
		return render(request, "piscine/piscine_manage_complete.html", {"task": "피신 유저의 정보를 업데이트 했습니다."})


class List(TemplateView):
	"""
	Rank42의 피시너 전체 랭킹 페이지
	"""
	template_name = "piscine/piscine_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		piscine_ft_users = PiscineFtUser.objects.filter(is_public=True).order_by('-piscine_level')

		context['piscine_ft_users'] = piscine_ft_users
		return context
