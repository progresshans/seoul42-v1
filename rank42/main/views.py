import requests, json

from django.shortcuts import render
from django.conf import settings
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views import View

from .custom import count_page, RankTier, FtApi, SuperUserCheckMixin
from .models import FtUser, Coalition, Tier


# Create your views here.
class ManagePage(SuperUserCheckMixin, TemplateView):
	template_name = "manage_page.html"


class MakeCoalition(SuperUserCheckMixin, View):
	def post(self, request):
		ft_api = FtApi()
		coalitions = ft_api.get_data(url="blocs/27")["coalitions"]
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
		ft_api = FtApi()
		page = count_page(ft_api.get_data(url="campus/29")["users_count"])
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


# FtUser에 있던 coalition 포인트를 Tier로 옮김 (추후 삭제)
class MoveCoalitionPoint(SuperUserCheckMixin, View):
	def post(self, request):
		ft_users = FtUser.objects.filter(is_alive=True)
		for ft_user in ft_users:
			tier = Tier(FtUser=ft_user, coalition_point=ft_user.coalition_point)
			if ft_user.coalition_point == 0:
				tier.name = "Unranked"
				tier.rank = 0
			tier.save()
		return render(request, "manage_complete.html", {"task":"MoveCoalitionPoint"})


class MainIndex(TemplateView):
	template_name = "main_index.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		ft_users = FtUser.objects.filter(is_alive=True).exclude(coalition_point=0).order_by('-coalition_point')
		unrank_ft_users = FtUser.objects.filter(is_alive=True, coalition_point=0)
		rank_tier = RankTier(ft_users.count())

		context['ft_users'], context['unrank_ft_users'] = rank_tier.set_tier(ft_users, unrank_ft_users)
		return context


class RankSearch(TemplateView):
	template_name = "rank_search.html"

	def get_context_data(self, **kwargs):
		context = super().get_context_data(**kwargs)
		login = self.request.GET.get('login', '')
		ft_users = FtUser.objects.filter(is_alive=True).exclude(coalition_point=0).order_by('-coalition_point')
		rank_tier = RankTier(ft_users.count())

		context['ft_user'] = rank_tier.set_tier(ft_users).get(login=login)
		return context