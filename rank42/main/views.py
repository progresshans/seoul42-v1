import requests, json
from django_pandas.io import read_frame
from typing import Dict, Any, Iterable

from django.shortcuts import render, redirect
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views import View
from django.urls import reverse

from .custom import count_page, SuperUserCheckMixin
from .ftapi import FtApi
from .rank import RankTier
from .models import FtUser, Coalition, Tier


# Create your views here.
class ManagePage(SuperUserCheckMixin, TemplateView):
	template_name = "manage_page.html"


class MakeCoalition(SuperUserCheckMixin, View):
	def post(self, request):
		"""

		:param request:
		:return:
		"""
		ft_api = FtApi()
		coalitions: Iterable[Dict[str, str]] = ft_api.get_data(url="blocs/27")["coalitions"]
		for coalition in coalitions:
			if Coalition.objects.filter(id=coalition["id"]).exists():
				pass
			else:
				Coalition.objects.create(
					id=coalition["id"],
					name=coalition["name"],
					color=coalition["color"],
				)
		return render(request, "manage_complete.html", {"task": "MakeCoalition"})


class MakeFtUser(SuperUserCheckMixin, View):
	def post(self, request):
		ft_api: FtApi = FtApi()
		page: int = count_page(ft_api.get_data(url="campus/29")["users_count"])
		crawlings = [ft_api.get_data(url="campus/29/users", page=x, per_page=100, sort="login") for x in range(1, int(page) + 1)]
		for crawling in crawlings:
			for data in crawling:
				if FtUser.objects.filter(id=data["id"]).exists():
					pass
				else:
					# detail_data = ft_api.get_data(url=f'users/{data.id}')
					coalition_data = ft_api.get_data(url=f'users/{data["id"]}/coalitions_users')
					if coalition_data and Coalition.objects.filter(id=int(coalition_data[0]["coalition_id"])).exists():
						FtUser.objects.create(
							id=data["id"],
							login=data["login"],
							is_alive=True,
							coalition=Coalition.objects.get(id=int(coalition_data[0]["coalition_id"])),
							coalition_point=coalition_data[0]["score"],
						)
					else:
						FtUser.objects.create(
							id=data["id"],
							login=data["login"],
							is_alive=False,
						)
		return render(request, "manage_complete.html", {"task": "MakeFtUser"})


# FtUser에 있던 coalition 포인트와 Tier 관련 데이터를 Tier로 옮김 (마이그레이션용, 추후 삭제)
class MoveCoalitionPoint(SuperUserCheckMixin, View):
	def post(self, request):
		ft_users: Iterable[FtUser] = FtUser.objects.filter(is_alive=True)
		for ft_user in ft_users:
			tier: Tier = Tier(FtUser=ft_user)
			tier.coalition_point = ft_user.coalition_point
			if ft_user.coalition_point == 0:
				tier.name = "Unranked"
				tier.rank = 0
			tier.save()
		return render(request, "manage_complete.html", {"task":"MoveCoalitionPoint"})


class Main(View):
	def get(self, request, **kwargs):
		if request.GET.get('login'):
			return redirect('search', login=request.GET.get('login'))
		return render(request, "main.html")


class List(TemplateView):
	template_name = "list.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		ft_users = FtUser.objects.filter(is_alive=True).exclude(coalition_point=0).order_by('-coalition_point')
		unrank_ft_users = FtUser.objects.filter(is_alive=True, coalition_point=0)
		rank_tier = RankTier(ft_users.count())

		context['ft_users'], context['unrank_ft_users'] = rank_tier.set_tier(ft_users, unrank_ft_users)
		return context


class Search(TemplateView):
	template_name = "search.html"

	@staticmethod
	def get_next_tier_name(ft_users, ft_user):
		for temp_user in ft_users:
			if temp_user.tier.tier_name != ft_user.tier.tier_name:
				return temp_user.tier.tier_name, temp_user.tier.coalition_point - ft_user.tier.coalition_point
		return 0, 0

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		login = kwargs['login']
		ft_users = FtUser.objects.filter(is_alive=True).order_by('-coalition_point')
		ft_user = ft_users.get(login=login)
		ft_user.percent = round((ft_user.tier.tier_rank / ft_users.count()) * 100, 1)
		if ft_user.tier.coalition_point != 0:
			ft_user.next_tier_name, ft_user.next_tier_point = self.get_next_tier_name(reversed(list(ft_users[:ft_user.tier.tier_rank - 1])), ft_user)
			ft_user.need_peer_evaluation = (ft_user.next_tier_point // 42) + 1
			ft_user.tier_img = RankTier().get_tier_img(ft_user.tier.tier_name)
		else:
			ft_user.next_tier_name, ft_user.next_tier_point = -1, -1

		context['ft_user'] = ft_user
		return context