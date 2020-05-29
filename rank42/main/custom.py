import requests
from django.conf import settings
from django.views import View
from django.contrib.auth.mixins import UserPassesTestMixin
from .models import Tier


def count_page(number):
	"""총 유저 수를 가지고 100으로 나눠 api가 파싱해야하는 총 페이지 수를 반환"""
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
	"""슈퍼 유저인지 확인하는 Mixin"""
	def test_func(self):
		return self.request.user.is_superuser


class RankTier:
	"""rank42에서 사용되는 티어 시스템 생산 및 수정 등 모든 부분을 관리하는 class"""
	challenger_name = "Challenger"
	challenger_per = 0.1
	challenger_img = "https://opgg-static.akamaized.net/images/medals/challenger_1.png"
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
	unranked_name = "Unranked"
	unranked_img = "https://opgg-static.akamaized.net/images/medals/default.png"

	def __init__(self, number=None):
		"""'number(캠퍼스의 본과 참여 학생수)'에 맞게 티어별 수를 생성"""
		if number:
			self.rank_users_number = int(number)
			self.challenger = round(number * (self.challenger_per / 100))
			self.master = round(number * (self.master_per / 100))
			self.diamond = round(number * (self.diamond_per / 100))
			self.platinum = round(number * (self.platinum_per / 100))
			self.gold = round(number * (self.gold_per / 100))
			self.silver = round(number * (self.silver_per / 100))
			self.bronze = number - (self.challenger + self.master + self.diamond + self.platinum + self.gold + self.silver)

	def make_tier_list(self):
		"""Tier 모델을 가지고 전체적으로 티어를 설정함"""
		pass


	def set_tier(self, ft_users, unrank_ft_users=None):
		"""
		본과 유저들의 queryset을 가지고 전체적으로 티어를 설정함

		:param ft_users: 점수가 존재하는 본과 유저 queryset
		:param unrank_ft_users: (선택)점수가 존재하지 않는 본과 유저 queryset
		:return: 본과 유저 queryset
		"""
		for i, ft_user in enumerate(ft_users):
			temp = {}
			tier = Tier(id=ft_user.id)
			if self.challenger >= i:
				temp["tier_name"] = self.challenger_name
			elif self.challenger + self.master >= i:
				temp["tier_name"] = self.master_name
			elif self.challenger + self.master + self.diamond >= i:
				temp["tier_name"] = self.diamond_name
			elif self.challenger + self.master + self.diamond + self.platinum >= i:
				temp["tier_name"] = self.platinum_name
			elif self.challenger + self.master + self.diamond + self.platinum + self.gold >= i:
				temp["tier_name"] = self.gold_name
			elif self.challenger + self.master + self.diamond + self.platinum + self.gold + self.silver >= i:
				temp["tier_name"] = self.silver_name
			else:
				temp["tier_name"] = self.bronze_name
			temp["tier_rank"] = i + 1
			if temp["tier_rank"] != tier.tier_rank or temp["tier_name"] != tier.tier_name:
				tier.tier_name = temp["tier_name"]
				tier.tier_rank = temp["tier_rank"]
				tier.save()

		# 점수가 존재하지 않는 본과 유저에 대해 처리할지는 선택 가능. 리턴값이 다름.
		if unrank_ft_users:
			for ft_user in unrank_ft_users:
				tier = Tier(id=ft_user.id)
				tier.tier_name = self.unranked_name
				tier.tier_img = self.unranked_img
				tier.tier_rank = 0
				tier.save()
			return ft_users, unrank_ft_users
		return ft_users

	def get_rank_users_number(self):
		"""class 생성시 'number(캠퍼스의 본과 참여 학생수)'에 입력된 값을 반환"""
		return self.rank_users_number
