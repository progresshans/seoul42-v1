import requests, json

from django.shortcuts import render
from django.conf import settings
from django.contrib.auth.mixins import UserPassesTestMixin
from django.views.generic.base import TemplateView
from django.views.generic.list import ListView
from django.views import View

from .custom import count_page, RankTier
from .models import FtUser, Coalition


# Create your views here.
class FtApi:
	ft_access_token = None
	ft_oauth_url = "https://api.intra.42.fr/oauth/token"
	ft_api_url = "https://api.intra.42.fr/v2/"
	update_branch = None

	def __init__(self, UpdateBranch=None):
		self.ft_uid_key = settings.FT_UID_KEY
		self.ft_secret_key = settings.FT_SECRET_KEY
		self.update_branch = UpdateBranch if UpdateBranch else None

	def get_access_token(self):
		oauth_data = {
			'grant_type': 'client_credentials',
			'client_id': self.ft_uid_key,
			'client_secret': self.ft_secret_key,
		}
		self.ft_access_token = requests.post(self.ft_oauth_url, data=oauth_data).json()['access_token']
		return self.ft_access_token

	def get_data(self, url, page=1, per_page=100, sort=None):
		params = {
			'access_token': self.get_access_token(),
			'page': page if page else '',
			'per_page': per_page if per_page else '',
			'sort': sort if sort else '',
		}
		return requests.get(f'{self.ft_api_url}{url}', params=params).json()


class SuperUserCheckMixin(UserPassesTestMixin, View):
	def test_func(self):
		return self.request.user.is_superuser


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


class MakeFtUser(SuperUserCheckMixin, View):
	def post(self, request):
		ft_api = FtApi()
		page = count_page(ft_api.get_data(url="campus/29")["users_count"])
		crawlings = [ft_api.get_data(url="campus/29/users", page=x, per_page=100, sort="login") for x in range(int(page))]
		for crawling in crawlings:
			for data in crawling:
				if FtUser.objects.filter(id=data["id"]).exists():
					pass
				else:
					# detail_data = ft_api.get_data(url=f'users/{data.id}')
					coalition_data = ft_api.get_data(url=f'users/{data["id"]}/coalitions')
					if coalition_data and Coalition.objects.filter(id=int(coalition_data[0]["id"])).exists():
						FtUser.objects.create(
							id=data["id"],
							login=data["login"],
							is_alive=True,
							coalition=Coalition.objects.get(id=int(coalition_data[0]["id"])),
							coalition_point=coalition_data[0]["score"],
						)
					else:
						FtUser.objects.create(
							id=data["id"],
							login=data["login"],
							is_alive=False,
						)


class MainIndex(ListView):
	context_object_name = "objects"
	template_name = "main_index.html"

	def get_queryset(self):
		ft_user = FtUser.objects.filter(is_alive=True).order_by('-coalition_point')
		rank_tier = RankTier(ft_user.count())

		queryset = {
			'ft_user': ft_user,
			'challenger': rank_tier.challenger,
			'grandmaster': rank_tier.grandmaster,
			'master': rank_tier.master,
			'diamond': rank_tier.diamond,
			'platinum': rank_tier.platinum,
			'gold': rank_tier.gold,
			'silver': rank_tier.silver,
			'bronze': rank_tier.bronze,
			'iron': rank_tier.iron,
		}
		return queryset