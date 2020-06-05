"""
42 api 호출을 위한 관련 코드
"""
from typing import Dict, Union, Iterable

import requests
from django.conf import settings


class FtApi:
	"""42api 파싱 class"""
	ft_access_token = None
	ft_oauth_url = "https://api.intra.42.fr/oauth/token"
	ft_api_url = "https://api.intra.42.fr/v2/"
	update_branch = None

	def __init__(self, UpdateBranch=None):
		self.ft_uid_key = settings.FT_UID_KEY
		self.ft_secret_key = settings.FT_SECRET_KEY
		self.update_branch = UpdateBranch if UpdateBranch else None

	def get_access_token(self) -> str:
		"""42api에 접속하기 위한 access_token을 반환"""
		oauth_data: Dict[str, str] = {
			'grant_type': 'client_credentials',
			'client_id': self.ft_uid_key,
			'client_secret': self.ft_secret_key,
		}
		self.ft_access_token: str = requests.post(self.ft_oauth_url, data=oauth_data).json()['access_token']
		return self.ft_access_token

	def get_data(self, url: str, page: int = 1, per_page: int = 100, sort: str = None) -> dict:
		"""
		42api를 통해 json 파싱 데이터를 반환

		:param url: 'https://api.intra.42.fr/apidoc' 참조, '/v2/'이후의 url
		:param page: 파싱할 페이지
		:param per_page: 페이지당 가져올 목록 개수
		:param sort: 정렬 기준
		:return: 42api json 파싱 데이터
		"""
		params: Dict[str, Union[str, int]] = {
			'access_token': self.get_access_token(),
			'page': page if page else '',
			'per_page': per_page if per_page else '',
			'sort': sort if sort else '',
		}
		return requests.get(f'{self.ft_api_url}{url}', params=params).json()
