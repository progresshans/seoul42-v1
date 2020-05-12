import requests
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin


def count_page(number):
	if int(number) <= 100:
		return 1
	page = int(number) / 100
	page = int(page) + 1 if number % (100 * int(page)) != 0 else int(page)
	return page


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


class RankTier:
	challenger_name = "Chanllenger"
	challenger_per = 0.1
	challenger_img = "https://opgg-static.akamaized.net/images/medals/challenger_1.png"
	grandmaster_name = "Grandmaster"
	grandmaster_per = 0.2
	grandmaster_img = "https://opgg-static.akamaized.net/images/medals/grandmaster_1.png"
	master_name = "Master"
	master_per = 0.4
	master_img = "https://opgg-static.akamaized.net/images/medals/master_1.png"
	diamond_name = "Diamond"
	diamond_per = 2.5
	diamond_img = "https://opgg-static.akamaized.net/images/medals/diamond_1.png"
	platinum_name = "Platinum"
	platinum_per = 8.3
	platinum_img = "https://opgg-static.akamaized.net/images/medals/platinum_1.png"
	gold_name = "Gold"
	gold_per = 24
	gold_img = "https://opgg-static.akamaized.net/images/medals/gold_1.png"
	silver_name = "Silver"
	silver_per = 35.2
	silver_img = "https://opgg-static.akamaized.net/images/medals/silver_1.png"
	bronze_name = "Bronze"
	bronze_per = 22.3
	bronze_img = "https://opgg-static.akamaized.net/images/medals/bronze_1.png"
	iron_name = "Iron"
	iron_per = 7.0
	iron_img = "https://opgg-static.akamaized.net/images/medals/iron_1.png"

	def __init__(self, number):
		self.challenger = round(number * (self.challenger_per / 100))
		self.grandmaster = round(number * (self.grandmaster_per / 100))
		self.master = round(number * (self.master_per / 100))
		self.diamond = round(number * (self.diamond_per / 100))
		self.platinum = round(number * (self.platinum_per / 100))
		self.gold = round(number * (self.gold_per / 100))
		self.silver = round(number * (self.silver_per / 100))
		self.bronze = round(number * (self.bronze_per / 100))
		self.iron = number - (self.challenger + self.grandmaster + self.master + self.diamond + self.platinum + self.gold + self.silver + self.bronze)

	def set_tier(self, ft_users):
		for i, ft_user in enumerate(ft_users):
			if self.challenger >= i:
				ft_user.tier_name = self.challenger_name
				ft_user.tier_img = self.challenger_img
			elif self.challenger + self.grandmaster >= i:
				ft_user.tier_name = self.grandmaster_name
				ft_user.tier_img = self.grandmaster_img
			elif self.challenger + self.grandmaster + self.master >= i:
				ft_user.tier_name = self.master_name
				ft_user.tier_img = self.master_img
			elif self.challenger + self.grandmaster + self.master + self.diamond >= i:
				ft_user.tier_name = self.diamond_name
				ft_user.tier_img = self.diamond_img
			elif self.challenger + self.grandmaster + self.master + self.diamond + self.platinum >= i:
				ft_user.tier_name = self.platinum_name
				ft_user.tier_img = self.platinum_img
			elif self.challenger + self.grandmaster + self.master + self.diamond + self.platinum + self.gold >= i:
				ft_user.tier_name = self.gold_name
				ft_user.tier_img = self.gold_img
			elif self.challenger + self.grandmaster + self.master + self.diamond + self.platinum + self.gold + self.silver >= i:
				ft_user.tier_name = self.silver_name
				ft_user.tier_img = self.silver_img
			elif self.challenger + self.grandmaster + self.master + self.diamond + self.platinum + self.gold + self.silver + self.bronze >= i:
				ft_user.tier_name = self.bronze_name
				ft_user.tier_img = self.bronze_img
			else:
				ft_user.tier_name = self.iron_name
				ft_user.tier_img = self.iron_img
			ft_user.tier_rank = i + 1
		return ft_users
