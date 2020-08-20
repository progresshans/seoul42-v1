"""
42 oauth 인증을 위한 코드
"""
from typing import Dict

import requests
from django.conf import settings


class FtAuthApi:
	"""42 oauth 인증을 위한 class"""
	ft_access_token = None
	ft_refresh_token = None
	ft_oauth_url = "https://api.intra.42.fr/oauth/token"
	ft_api_url = "https://api.intra.42.fr/v2/"

	def __init__(self):
		self.ft_uid_key = settings.FT_UID_KEY
		self.ft_secret_key = settings.FT_SECRET_KEY

	def set_access_token(self, code, redirect_url) -> int:
		"""42api에 접속하기 위한 access_token을 반환"""
		oauth_data: Dict[str, str] = {
			'grant_type': 'authorization_code',
			'client_id': self.ft_uid_key,
			'client_secret': self.ft_secret_key,
			'code': code,
			'redirect_uri': redirect_url,
		}
		try:
			ft_api_result = requests.post(self.ft_oauth_url, data=oauth_data).json()
			self.ft_access_token = ft_api_result['access_token']
			self.ft_refresh_token = ft_api_result['refresh_token']
			return 1
		except KeyError:
			return 0

	def get_access_token(self) -> str:
		return self.ft_access_token

	def get_refresh_token(self):
		return self.ft_refresh_token

	def get_me(self):
		params: dict = {
			'access_token': self.get_access_token(),
		}
		return requests.get(f"{self.ft_api_url}me", params=params).json()

	def get_data(self, url: str, page: int = 1, per_page: int = 100, sort: str = None) -> dict:
		"""
		42api를 통해 json 파싱 데이터를 반환

		:param url: 'https://api.intra.42.fr/apidoc' 참조, '/v2/'이후의 url
		:param page: 파싱할 페이지
		:param per_page: 페이지당 가져올 목록 개수
		:param sort: 정렬 기준
		:return: 42api json 파싱 데이터
		"""
		params: dict = {
			'access_token': self.get_access_token(),
			'page': page if page else '',
			'per_page': per_page if per_page else '',
			'sort': sort if sort else '',
		}
		return requests.get(f'{self.ft_api_url}{url}', params=params).json()