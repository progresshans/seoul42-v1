from decimal import Decimal
from .models import PiscineFtUser


class FtApiAsync:
	def __init__(self, data, ft_api):
		self.ft_api = ft_api
		self.data = data

	def run(self):
		detail_data = self.ft_api.get_data(url=f'users/{self.data["id"]}')
		if len(detail_data["cursus_users"]) == 1 and not detail_data["cursus_users"][0]["end_at"] is None:
			# peer_list = ft_api.get_data(
			# 	url=f'users/{data["id"]}/scale_teams/graph/on/created_at/by/day'
			# )
			PiscineFtUser.objects.create(
				id=self.data["id"],
				login=self.data["login"],
				pool_year=detail_data["pool_year"],
				pool_month=detail_data["pool_month"],
				is_public=True,
				piscine_level=Decimal(detail_data["cursus_users"][0]["level"]),
				# peer_count=get_piscine_value_sum(peer_list)
			)


def use_ft_api(args):
	FtApiAsync(args["data"], args["ft_api"]).run()
