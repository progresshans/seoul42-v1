from celery import shared_task
from main.ftapi import FtApi
from main.models import FtUser, Coalition, Tier


@shared_task()
def make_ft_user(page):
	ft_api = FtApi()
	users = ft_api.get_data(url="campus/29/users", page=page, per_page=100, sort="login")
	for data in users:
		try:
			FtUser.objects.get(id=data["id"])
		except:
			try:
				# detail_data = ft_api.get_data(url=f'users/{data["id"]}')
				coalition_data = ft_api.get_data(url=f'users/{data["id"]}/coalitions_users')
				if coalition_data and Coalition.objects.filter(id=int(coalition_data[0]["coalition_id"])).exists():
					ft_user = FtUser.objects.create(
						id=data["id"],
						login=data["login"],
						is_alive=True,
						coalition=Coalition.objects.get(id=int(coalition_data[0]["coalition_id"])),
					)
					Tier.objects.create(
						FtUser=ft_user,
						coalition_point=coalition_data[0]["score"],
					)
				else:
					FtUser.objects.create(
						id=data["id"],
						login=data["login"],
						is_alive=False,
					)
			except:
				pass
