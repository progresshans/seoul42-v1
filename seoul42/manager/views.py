from typing import Dict, Iterable

from django.shortcuts import render
from django.views.generic.base import TemplateView
from django.views import View

from main.customs import count_page, SuperUserCheckMixin
from main.ftapi import FtApi
from main.models import FtUser, Coalition, Tier

from .tasks import make_ft_user


class ManagePage(SuperUserCheckMixin, TemplateView):
	template_name = "manager/manage_page.html"


class MakeCoalition(SuperUserCheckMixin, View):
	"""
	27 blocs에 있는 특정 Coalition을 만
	"""
	def post(self, request):
		ft_api = FtApi()
		coalitions: Iterable[Dict[str, str]] = ft_api.get_data(url="blocs/27")["coalitions"]
		for coalition in coalitions:
			if Coalition.objects.filter(id=coalition["id"]).exists():
				pass
			else:
				Coalition.objects.create(
					id=coalition["id"],
					name=coalition["name"],
					color=coalition["color"],
				)
		return render(request, "manager/manage_complete.html", {"task": "MakeCoalition"})


class MakeFtUser(SuperUserCheckMixin, View):
	"""
	42 한국 캠퍼스 유저들을 생성함
	"""
	def post(self, request):
		ft_api: FtApi = FtApi()
		pages = count_page(ft_api.get_data(url="campus/29")["users_count"])
		for page in range(1, int(pages) + 1):
			make_ft_user.delay(page)
		return render(request, "manager/manage_complete.html", {"task": "MakeFtUser"})


# FtUser에 있던 coalition 포인트와 Tier 관련 데이터를 Tier로 옮김 (마이그레이션용, 추후 삭제)
class MoveCoalitionPoint(SuperUserCheckMixin, View):
	def post(self, request):
		ft_users: Iterable[FtUser] = FtUser.objects.filter(is_alive=True)
		for ft_user in ft_users:
			tier: Tier = Tier(FtUser=ft_user)
			tier.coalition_point = ft_user.coalition_point
			if ft_user.coalition_point == 0:
				tier.name = "Unranked"
				tier.rank = 0
			tier.save()
		return render(request, "manager/manage_complete.html", {"task": "MoveCoalitionPoint"})