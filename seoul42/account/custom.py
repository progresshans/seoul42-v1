import string
import random
from .ftauthapi import FtAuthApi


def get_random_string(length):
	return ''.join(random.choice(string.ascii_letters + string.digits) for _ in range(length))


def authenticating_ft_api(code, redirect_url):
	ft_auth_api = FtAuthApi()
	if not ft_auth_api.set_access_token(code, redirect_url):
		return None, None
	ft_user_data = ft_auth_api.get_me()
	return ft_auth_api, ft_user_data
