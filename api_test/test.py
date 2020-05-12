import requests, json

oauth_data = {
	'grant_type': 'client_credentials',
	'client_id': '20a94ea0961be7f69ed5554cb250a55efe9109bb31a93c63744299eee41aac4d',
	'client_secret': 'c7257e57a584e98b971996696badd424d8bc16bea0c839633bc5b83566edf8f7',
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

def count_page(number):
	if int(number) <= 100:
		return 1
	page = int(number) / 100
	page = int(page) + 1 if number % (100 * int(page)) != 0 else int(page)
	return page

print(requests.get(f'{api_url}campus/29', params={'access_token': access_token}).json()["users_count"])