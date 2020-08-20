import requests, json, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_INFO_FILE = os.path.join(BASE_DIR, 'seoul42', 'config', 'settings', 'secret_info_file.json')
with open(SECRET_INFO_FILE) as f:
	secrets = json.loads(f.read())


def get_secret(setting, secrets=secrets):
	try:
		return secrets[setting]
	except KeyError:
		print(f"Set the {setting} environment variable")


oauth_data = {
	'grant_type': 'client_credentials',
	'client_id': get_secret("FT_UID_KEY"),
	'client_secret': get_secret("FT_SECRET_KEY"),
}
oauth_url = "https://api.intra.42.fr/oauth/token"
api_url = "https://api.intra.42.fr/v2/"


class FtApi:
	"""42api 파싱 class"""
	ft_access_token = None
	ft_oauth_url = "https://api.intra.42.fr/oauth/token"
	ft_api_url = "https://api.intra.42.fr/v2/"
	update_branch = None

	def __init__(self):
		self.ft_uid_key = get_secret("FT_UID_KEY")
		self.ft_secret_key = get_secret("FT_SECRET_KEY")

	def get_access_token(self):
		"""42api에 접속하기 위한 access_token을 반환"""
		oauth_data = {
			'grant_type': 'client_credentials',
			'client_id': self.ft_uid_key,
			'client_secret': self.ft_secret_key,
		}
		self.ft_access_token = requests.post(self.ft_oauth_url, data=oauth_data).json()['access_token']
		return self.ft_access_token

	def get_data(self, url, page=1, per_page=100, sort=None):
		"""
		42api를 통해 json 파싱 데이터를 반환

		:param url: 'https://api.intra.42.fr/apidoc' 참조, '/v2/'이후의 url
		:param page: 파싱할 페이지
		:param per_page: 페이지당 가져올 목록 개수
		:param sort: 정렬 기준
		:return: 42api json 파싱 데이터
		"""
		params = {
			'access_token': self.get_access_token(),
			'page': page if page else '',
			'per_page': per_page if per_page else '',
			'sort': sort if sort else '',
		}
		return requests.get(f'{self.ft_api_url}{url}', params=params).json()


oauth_request = requests.post(oauth_url, data=oauth_data)
print(oauth_request.json())
access_token = oauth_request.json()['access_token']

# print(requests.get(f'{api_url}campus/29/users', params={'access_token': access_token}).json())
# try:
# 	print(requests.get(f'{api_url}users/72500', params={'access_token': access_token}).json()["cursus_users"][1])
# except IndexError:
# 	print("본과 사람이 아님.")
# print(requests.get(f'{api_url}users/68944', params={'access_token': access_token}).json()["cursus_users"][1]["blackholed_at"])
# print(requests.get(f'{api_url}users/68944', params={'access_token': access_token}).json())
#
# data = requests.get(f'{api_url}campus/29/users', params={'access_token': access_token, 'sort': "login"}).json()
# for i in data:
# 	print(i['id'])
#
# datas = [requests.get(f'{api_url}campus/29/users', params={'access_token': access_token, 'page' : x, 'sort': "login"}).json() for x in range(4)]
# for data in datas:
# 	print(data)
#
# coals = requests.get(f'{api_url}blocs/27', params={'access_token': access_token}).json()["coalitions"]
# for i in coals:
# 	print(i["id"])
#
# print(requests.get(f'{api_url}campus/29', params={'access_token': access_token}).json()["users_count"])
#
# print(requests.get(f'{oauth_url}/info', params={'access_token': access_token}).json())

# def count_page(number):
# 	if int(number) <= 100:
# 		return 1
# 	page = int(number) / 100
# 	page = int(page) + 1 if number % (100 * int(page)) != 0 else int(page)
# 	return page

# print(requests.get(f'{api_url}users/hhan/scale_teams/graph/on/created_at/by/day', params={'access_token': access_token}).json())
print(requests.get(f'{api_url}users/heryu', params={'access_token': access_token}).json())

ft_api = FtApi()
users = ft_api.get_data(url="campus/29/users", page=3, per_page=100, sort="login")
for user in users:
	print(user)


def count_page(number: int) -> int:
	"""총 유저 수를 가지고 100으로 나눠 api가 파싱해야하는 총 페이지 수를 반환"""
	if int(number) <= 100:
		return 1
	page: float = int(number) / 100
	page: int = int(page) + 1 if number % (100 * int(page)) != 0 else int(page)
	return page

print(count_page(ft_api.get_data(url="campus/29")["users_count"]))