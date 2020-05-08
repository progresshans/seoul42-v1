import requests, json

oauth_data = {
	'grant_type' : 'client_credentials',
	'client_id' : '20a94ea0961be7f69ed5554cb250a55efe9109bb31a93c63744299eee41aac4d',
	'client_secret' : 'c7257e57a584e98b971996696badd424d8bc16bea0c839633bc5b83566edf8f7',
}
oauth_url = "https://api.intra.42.fr/oauth/token"

access_token = requests.post(oauth_url, data=oauth_data)
print(access_token.json())