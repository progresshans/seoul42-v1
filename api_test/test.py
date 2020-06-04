import requests, json, os

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SECRET_INFO_FILE = os.path.join(BASE_DIR, 'rank42', 'config', 'settings', 'secret_info_file.json')
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

oauth_request = requests.post(oauth_url, data=oauth_data)
access_token = oauth_request.json()['access_token']
print(oauth_request.json())

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

print(requests.get(f'{api_url}events/4579', params={'access_token': access_token}).json())