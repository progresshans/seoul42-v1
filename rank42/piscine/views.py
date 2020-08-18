from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View
from datetime import datetime, timedelta
from decimal import Decimal

from main.custom import count_page, SuperUserCheckMixin
from main.ftapi import FtApi
from .customs import AllowPiscineListCheckMixin
from .models import PiscineFtUser, PiscineProject, TempFtUser
from .tasks import make_piscine_ft_user


class PiscineManagePage(SuperUserCheckMixin, TemplateView):
	template_name = "piscine/piscine_manage_page.html"


def get_piscine_value_sum(peer_list):
	result = 0
	for _, value in peer_list.items():
		result += int(value)
	return result


class MakePiscineFtUser(SuperUserCheckMixin, View):
	"""
	42 한국 캠퍼스 유저들중 피신중인 유저를 생성함
	"""

	def post(self, request):
		ft_api = FtApi()
		pages = count_page(ft_api.get_data(url="campus/29")["users_count"])
		for page in range(1, int(pages) + 1):
			make_piscine_ft_user.delay(page)
		return render(request, "piscine/piscine_manage_complete.html", {"task": "MakePiscineFtUser"})


class DeletePiscineFtUser(SuperUserCheckMixin, View):
	def post(self, request):
		PiscineFtUser.objects.all().delete()
		return render(request, "piscine/piscine_manage_complete.html", {"task": "DeletePiscineFtUser"})


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
		piscine_ft_users = PiscineFtUser.objects.filter(is_public=True, pool_year="2020", pool_month="july")
		for piscine_ft_user in piscine_ft_users:
			if self.is_one_hour(piscine_ft_user.updated_at):
				detail_data = ft_api.get_data(url=f'users/{piscine_ft_user.id}')
				# peer_list = ft_api.get_data(
				# 	url=f'users/{piscine_ft_user.id}/scale_teams/graph/on/created_at/by/day'
				# )
				piscine_ft_user.piscine_level = Decimal(detail_data["cursus_users"][0]["level"])
				# piscine_ft_user.peer_count = get_piscine_value_sum(peer_list)
				if len(detail_data["cursus_users"]) == 2:
					piscine_ft_user.is_pass = True
				piscine_ft_user.save()
		return render(request, "piscine/piscine_manage_complete.html", {"task": "피신 유저의 정보를 업데이트 했습니다."})


class List(AllowPiscineListCheckMixin, TemplateView):
	"""
	Rank42의 피시너 전체 랭킹 페이지
	"""
	template_name = "piscine/piscine_list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		pool_year = "2020" if self.request.GET.get('pool_year') is None else self.request.GET.get('pool_year')
		pool_month = "july" if self.request.GET.get('pool_month') is None else self.request.GET.get('pool_month')

		piscine_ft_users = PiscineFtUser.objects.filter(is_public=True, pool_year=pool_year, pool_month=pool_month).order_by('-piscine_level')
		context['sort_value'] = '레벨'
		if pool_year == "2020" and pool_month == "february":
			context['piscine_name'] = '1기 1차'
		elif pool_year == "2020" and pool_month == "june":
			context['piscine_name'] = '1기 2차'
		elif pool_year == "2020" and pool_month == "july":
			context['piscine_name'] = '2기 1차'
		elif pool_year == "2020" and pool_month == "august":
			context['piscine_name'] = '2기 2차'

		# if self.request.GET.get('value') == 'level':
		# 	piscine_ft_users = PiscineFtUser.objects.filter(is_public=True, pool_year="2020", pool_month="july").order_by('-piscine_level')
		# 	context['sort_value'] = '레벨'
		# else:
		# 	piscine_ft_users = PiscineFtUser.objects.filter(is_public=True, pool_year="2020", pool_month="july").order_by('-peer_count')
		# 	context['sort_value'] = '평가횟수'

		context['piscine_ft_users'] = piscine_ft_users
		return context


class Index(TemplateView):
	template_name = "piscine/piscine_index.html"
