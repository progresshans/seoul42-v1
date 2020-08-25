from celery import shared_task
from main.ftapi import FtApi
from main.customs import count_page
from .models import PiscineFtUser
from decimal import Decimal


@shared_task()
def make_piscine_ft_user(page):
	ft_api = FtApi()
	users = ft_api.get_data(url="campus/29/users", page=page, per_page=100, sort="login")
	for data in users:
		try:
			PiscineFtUser.objects.get(id=data["id"])
		except:
			try:
				detail_data = ft_api.get_data(url=f'users/{data["id"]}')
				if not detail_data["cursus_users"][0]["end_at"] is None:
					# peer_list = ft_api.get_data(
					# 	url=f'users/{data["id"]}/scale_teams/graph/on/created_at/by/day'
					# )
					if len(detail_data["cursus_users"]) == 2:
						PiscineFtUser.objects.create(
							id=data["id"],
							login=data["login"],
							pool_year=detail_data["pool_year"],
							pool_month=detail_data["pool_month"],
							is_public=True,
							is_pass=True,
							piscine_level=Decimal(detail_data["cursus_users"][0]["level"]),
							# peer_count=get_piscine_value_sum(peer_list)
						)
					else:
						PiscineFtUser.objects.create(
							id=data["id"],
							login=data["login"],
							pool_year=detail_data["pool_year"],
							pool_month=detail_data["pool_month"],
							is_public=True,
							is_pass=False,
							piscine_level=Decimal(detail_data["cursus_users"][0]["level"]),
							# peer_count=get_piscine_value_sum(peer_list)
						)
			except:
				pass
